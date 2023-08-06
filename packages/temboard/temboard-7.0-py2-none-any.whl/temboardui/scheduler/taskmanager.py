import sys
import time
import uuid
import logging
import json
import os.path
import types
import signal
from select import select, error as SelectError
from datetime import datetime, timedelta
from collections import deque
from multiprocessing import Process, Queue
from multiprocessing.connection import Listener, Client, AuthenticationError

try:
    from Queue import Empty
except ImportError:
    from queue import Empty

TM_WORKERS = []
TM_BOOTSTRAP = []
TM_SIGHUP = False
TM_SIGTERM = False
TM_SIGABRT = False

TM_DEF_LISTENER_ADDR = '/tmp/.temboardsched.sock'

# Message types
MSG_TYPE_TASK_NEW = 0
MSG_TYPE_TASK_STATUS = 1
MSG_TYPE_TASK_CANCEL = 2
MSG_TYPE_TASK_ABORT = 3
MSG_TYPE_TASK_LIST = 4
MSG_TYPE_RESP = 5
MSG_TYPE_ERROR = 6
MSG_TYPE_CONTEXT = 7

# Task status
TASK_STATUS_DEFAULT = 1
TASK_STATUS_SCHEDULED = 2
TASK_STATUS_QUEUED = 4
TASK_STATUS_DOING = 8
TASK_STATUS_DONE = 16
TASK_STATUS_FAILED = 32
TASK_STATUS_CANCELED = 64
TASK_STATUS_ABORTED = 128
TASK_STATUS_ABORT = 256

logger = logging.getLogger(__name__)


def json_serial_datetime(obj):
    # JSON serializer for datetime
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def make_worker_definition(function, pool_size):
    return {
        'name': function.__name__,
        'pool_size': pool_size,
        'module': function.__module__,
        'function': function.__name__
    }


def worker(pool_size=1):
    # Decorator that defines a new worker function
    def defines_worker(function):
        global TM_WORKERS
        TM_WORKERS.append(make_worker_definition(function, pool_size))
        return function

    return defines_worker


def handler_sigterm(num, frame):
    global TM_SIGTERM
    TM_SIGTERM = True


def handler_sighup(num, frame):
    global TM_SIGHUP
    TM_SIGHUP = True


def handler_sigabrt(num, frame):
    global TM_SIGABRT
    TM_SIGABRT = True


def bootstrap():
    def defines_bootstrap(function):
        global TM_BOOTSTRAP
        TM_BOOTSTRAP.append({
            'module': function.__module__,
            'function': function.__name__
        })
        return function

    return defines_bootstrap


def schedule_task(worker_name, id=None, options=None, start=None,
                  redo_interval=None, listener_addr=TM_DEF_LISTENER_ADDR,
                  authkey=None, expire=3600):
    # Schedule a new task
    return TaskManager.send_message(
                listener_addr,
                Message(
                    MSG_TYPE_TASK_NEW,
                    Task(
                        id=id,
                        worker_name=worker_name,
                        options=options,
                        start_datetime=start or datetime.utcnow(),
                        redo_interval=redo_interval,
                        expire=expire,
                    )
                ),
                authkey=authkey
           )


def set_context(k, v, listener_addr=TM_DEF_LISTENER_ADDR, authkey=None):
    # Update a context variable
    return TaskManager.send_message(
                listener_addr,
                Message(
                    MSG_TYPE_CONTEXT,
                    {k: v}
                ),
                authkey=authkey
           )


class Task(object):

    def __init__(self, worker_name=None, options=None, id=None,
                 status=TASK_STATUS_DEFAULT, start_datetime=None,
                 redo_interval=None, stop_datetime=None, output=None,
                 expire=3600):
        self.worker_name = worker_name
        self.options = options
        self.status = status
        self.start_datetime = start_datetime or datetime.utcnow()
        self.redo_interval = redo_interval
        self.stop_datetime = stop_datetime
        self.id = id
        self.output = output
        # Task expiration timeout in seconds.
        # Ended Tasks are removed from memory when current time exceeds
        # self.stop_datetime + self.expire.
        self.expire = expire

    def __repr__(self):
        return str(self.__dict__)


class Message(object):

    def __init__(self, type, content):
        self.type = type,
        self.content = content

    def __repr__(self):
        return str(self.__dict__)


class TaskList(object):

    def __init__(self, path):
        self.path = path
        self.tasks = dict()

    def _backup(self):
        if not self.path:
            return
        with open(self.path, 'w') as f:
            for _, t in self.tasks.items():
                try:

                    # Convert output to string if not a JSON serializable type
                    if type(t.output) not in (list, dict, str, type(None)):
                        t.output = str(t.output)

                    f.write(
                        json.dumps(
                            t.__dict__,
                            default=json_serial_datetime
                        ) + '\n'
                    )
                except TypeError:
                    # Could not serialize Task to JSON
                    logger.debug(t)
                    logger.error("Could not serialize Task to JSON")
                except Exception as e:
                    logger.exception(str(e))
                    logger.error("Could not write recovery file")

    def recover(self):
        if not self.path:
            return

        if not os.path.exists(self.path):
            return

        with open(self.path, 'r') as f:
            for l in f.readlines():
                try:
                    raw_dict = json.loads(l)
                    t = Task(
                            worker_name=raw_dict.get('worker_name'),
                            options=raw_dict.get('options'),
                            id=raw_dict.get('id'),
                            status=raw_dict.get('status'),
                            start_datetime=raw_dict.get('start_datetime'),
                            stop_datetime=raw_dict.get('stop_datetime'),
                            output=raw_dict.get('output'),
                            redo_interval=raw_dict.get('redo_interval')
                    )
                    # Convert isoformat to datetime
                    for a in ('start_datetime', 'stop_datetime'):
                        if getattr(t, a):
                            dt = datetime.strptime(getattr(t, a),
                                                   "%Y-%m-%dT%H:%M:%S.%f")
                            setattr(t, a, dt)

                    if t.status & TASK_STATUS_DOING:
                        # reset status & stop_datetime because the job was
                        # running the last time task list was synced.
                        t.status = TASK_STATUS_ABORTED
                        t.stop_datetime = datetime.utcnow()

                    if t.status & TASK_STATUS_SCHEDULED:
                        # reset status to default
                        t.status = TASK_STATUS_DEFAULT

                    logger.debug("SCHED: Recovered Task=%s" % t)
                    self.push(t)
                except Exception as e:
                    logger.error("Could not unserialize Task from JSON")
                    logger.debug(l)
                    logger.exception(e)

    def push(self, t):
        # Add a new task to the list
        if not t.id:
            t.id = self._gen_task_id()
        if t.id in self.tasks:
            raise KeyError("Task with id=%s already present" % t.id)
        self.tasks[t.id] = t
        # Save task list on disk
        self._backup()
        return t.id

    def get(self, task_id):
        if task_id not in self.tasks:
            raise Exception("Task id=%s not found" % task_id)
        return self.tasks[task_id]

    def update(self, task_id, **kwargs):
        if task_id not in self.tasks:
            raise Exception("Task id=%s not found" % task_id)
        t = self.tasks[task_id]
        for k, v in kwargs.items():
            try:
                getattr(t, k)
            except AttributeError:
                raise Exception("Task attribute %s does not exist" % k)
            setattr(t, k, v)
        self.tasks[task_id] = t
        # Save task list on disk
        self._backup()

    def rm(self, task_id):
        if task_id not in self.tasks:
            raise Exception("Task id=%s not found" % task_id)
        del(self.tasks[task_id])
        # Save task list on disk
        self._backup()

    def _gen_task_id(self):
        id = None
        while id is None or id in self.tasks:
            id = str(uuid.uuid4())[0:8]
        return id

    def get_n_todo(self):
        # Return the number of ongoing tasks (QUEUED | DOING)
        n = 0
        for id, task in self.tasks.items():
            if task.status & (TASK_STATUS_QUEUED | TASK_STATUS_DOING):
                n += 1
        return n


class TaskManager(object):

    def __init__(self, address=TM_DEF_LISTENER_ADDR, task_path=None,
                 authkey=None):

        self.scheduler = Scheduler(address, task_path, authkey)

    def set_context(self, key, val):
        self.scheduler.set_context(key, val)

    def start(self):
        logger.info("Starting TaskManager")
        self.scheduler.start()

    def restart(self, abort=False):
        if abort:
            self.stop()
            self.start()
        else:
            self.shutdown()
            self.start()

    def shutdown(self):
        # Will stop the scheduler and WP only when all the ongoing task are
        # done.
        logger.info("Shutting down scheduler")
        os.kill(self.scheduler.process.pid, signal.SIGTERM)
        self.join()

    def stop(self):
        # Abort all ongoing tasks and stop the scheduler and WP
        logger.info("Aborting scheduler")
        os.kill(self.scheduler.process.pid, signal.SIGABRT)
        self.join()

    def join(self):
        try:
            logger.debug("Joining processes")
            self.scheduler.process.join()
            self.scheduler.worker_pool.process.join()
        except KeyboardInterrupt:
            logger.debug("KeyboardInterrupt")
            return

    @staticmethod
    def send_message(address, message, authkey=''):
        conn = Client(address, authkey=authkey)
        conn.send(message)
        res = conn.recv()
        conn.close()
        return res


class Scheduler(object):

    def __init__(self, address, task_path, authkey):
        # Process objet from multiprocessing
        self.process = None
        # Listener for TM -> Scheduler IPC
        self.listener = None
        # Listener address
        self.address = address
        # Listener authentication key
        self.authkey = authkey
        # Path to TaskList on disk image file
        self.task_path = task_path
        # Queue used to send Task orders (start, stop) to WorkerPool
        self.task_queue = None
        # Queue used to notify Scheduler about Task status
        self.event_queue = None
        self.task_list = None
        self.context = dict()
        self.worker_pool = None
        self.shutdown = None

    def set_context(self, key, val):
        self.context[key] = val

    def get_context(self):
        return self.context

    def handle_listener_message(self):
        # read message from the listener
        try:
            conn = self.listener.accept()
        except AuthenticationError as e:
            logger.exception(e)
            logger.error("Authentication failed")
            return

        try:
            message = conn.recv()
        except Exception as e:
            conn.close()
            logger.exception(e)
            logger.error("Unable to read the message")
            return

        message.type = message.type[0]
        logger.debug("Received Message=%s" % message)

        # handle incoming message and return a response
        res = self.handle_message(message)
        conn.send(res)
        conn.close()

    def handle_event_queue_message(self):
        # read message from the event queue
        try:
            message = self.event_queue.get(False)
        except Empty:
            # should not happen
            logger.error("Event queue empty")
            return

        message.type = message.type[0]
        logger.debug("Received Message=%s" % message)

        # handle incoming message
        self.handle_message(message)

    def sync_bootstrap_options(self):
        # Reload bootstrap Task options and update Task from task_list with new
        # options. This is usefull to reflect context changes into Task options
        # like in a configuration update case.
        for bs_func in TM_BOOTSTRAP:
            func = getattr(sys.modules[bs_func['module']],
                           bs_func['function'])(context=self.get_context())
            if isinstance(func, types.GeneratorType):
                for t in func:
                    if isinstance(t, Task):
                        try:
                            self.task_list.update(
                                    t.id,
                                    options=t.options,
                                    redo_interval=t.redo_interval,
                            )
                        except Exception as e:
                            logger.exception(str(e))
                            logger.error("Could not update Task %s with"
                                         " options=%s" % (t.id, t.options))
                    else:
                        logger.error("Bootstrap task not Task instance")
            else:
                logger.error("Bootstrap function %s.%s not a generator"
                             % (bs_func['module'], bs_func['function']))

    def bootstrap(self):
        # Load Tasks from generators decorated by @taskmanager.bootstrap()
        for bs_func in TM_BOOTSTRAP:
            func = getattr(sys.modules[bs_func['module']],
                           bs_func['function'])(context=self.get_context())
            if isinstance(func, types.GeneratorType):
                for t in func:
                    if isinstance(t, Task):
                        try:
                            self.task_list.push(t)
                            logger.debug("Bootstrap Task=%s loaded" % t)
                        except KeyError:
                            logger.debug("Update Task %s with options=%s"
                                         % (t.id, t.options))
                            self.task_list.update(t.id, options=t.options)
                    else:
                        logger.error("Bootstrap task not Task instance")
            else:
                logger.error("Bootstrap function %s.%s not a generator"
                             % (bs_func['module'], bs_func['function']))

    def setup(self):
        # Need to shutdown ?
        self.shutdown = False
        # Instanciate a new Listener
        self.listener = Listener(self.address, family='AF_UNIX',
                                 authkey=self.authkey)
        # bootstrap
        self.bootstrap()
        # TODO
        # self.sync_bootstrap_options()
        self.select_timeout = 1

    def serve1(self):
        timeout = 1
        date_end = float(time.time()) + timeout

        logger.debug("Select on Listener with t=%s", self.select_timeout)

        # wait for I/O on Listener and event Queue
        try:
            fds, _, _ = select(
                [self.listener._listener._socket.fileno(),
                 self.event_queue._reader.fileno()],
                [], [], self.select_timeout)
        except SelectError as e:
            errno, message = e.args
            if errno == os.errno.EINTR:
                # Interrupted by e.g. SIGHUP. Just stop.
                return
            else:
                raise

        if len(fds) > 0:
            for fd in fds:
                if fd == self.listener._listener._socket.fileno():
                    if self.shutdown:
                        # during shutdown we don't handle incoming
                        # message anymore
                        continue
                    self.handle_listener_message()
                elif fd == self.event_queue._reader.fileno():
                    self.handle_event_queue_message()

            self.select_timeout = date_end - float(time.time())
            if self.select_timeout < 0:
                self.select_timeout = timeout
                date_end = float(time.time()) + timeout
        else:
            # we are here every 1 second
            logger.debug("Scheduling")
            # schedule Tasks & maintain Tasks list
            self.schedule()

            # reinit select timeout value
            self.select_timeout = timeout
            date_end = float(time.time()) + timeout

    def setup_task_list(self):
        # Instanciate TaskList
        self.task_list = TaskList(self.task_path)
        # recover tasks from on disk image
        self.task_list.recover()

    def run(self):
        # Add signal handlers
        signal.signal(signal.SIGTERM, handler_sigterm)
        signal.signal(signal.SIGHUP, handler_sighup)
        signal.signal(signal.SIGABRT, handler_sigabrt)

        global TM_SIGHUP
        global TM_SIGTERM
        global TM_SIGABRT

        self.setup_task_list()
        self.setup()
        while True:
            try:
                self.serve1()

                if TM_SIGTERM:
                    # We perform shutdown on SIGTERM: we wait until all
                    # ongoing tasks are done before stopping
                    logger.debug("SIGTERM received")
                    self.shutdown = True
                    TM_SIGTERM = False
                if TM_SIGHUP:
                    logger.debug("SIGHUP received")
                    self.sync_bootstrap_options()
                    TM_SIGHUP = False

                if TM_SIGABRT:
                    logger.debug("SIGABRT received")
                    TM_SIGABRT = False
                    self.stop()
                    return

                try:
                    # Check parent
                    os.kill(os.getppid(), 0)
                except Exception:
                    self.stop()
                    return

                if self.shutdown and self.task_list.get_n_todo() == 0:
                    # When shutting down, if there is no more ongoing task
                    # then we can stop
                    self.stop()
                    return

            except KeyboardInterrupt:
                logger.error("KeyboardInterrupt")
                self.stop()
                return
            except Exception as e:
                logger.exception(e)
                self.stop()
                return

    def schedule(self):
        now = datetime.utcnow()
        remove_list = []
        for task_id, t in self.task_list.tasks.items():

            start = t.start_datetime
            redo = t.redo_interval

            if not self.shutdown and start < now \
                    and t.status & TASK_STATUS_DEFAULT:
                # new task
                t.status = TASK_STATUS_SCHEDULED
                self.task_list.tasks[task_id] = t
                logger.debug("Pushing to WorkerPool Task=%s" % t)
                self.task_queue.put(t, False)
                continue

            if not self.shutdown \
                    and (redo and start + timedelta(seconds=redo) < now
                         and t.status & (TASK_STATUS_DONE | TASK_STATUS_FAILED
                                         | TASK_STATUS_ABORTED)):
                # redo task
                # update task attributes
                t.status = TASK_STATUS_SCHEDULED
                t.start_datetime = now
                t.stop_datetime = None
                t.output = None
                self.task_list.tasks[task_id] = t
                # push the task to the worker pool
                self.task_queue.put(t, False)
                continue

            if (not redo and t.stop_datetime and
                    t.stop_datetime + timedelta(seconds=t.expire) < now and
                    t.status & (TASK_STATUS_DONE | TASK_STATUS_FAILED |
                                TASK_STATUS_ABORTED |
                                TASK_STATUS_CANCELED)):
                # remove old tasks
                remove_list.append(t.id)
                continue

        for task_id in remove_list:
                logger.debug("Removing Task %s" % task_id)
                self.task_list.rm(task_id)

    def handle_message(self, message):
        if message.type == MSG_TYPE_TASK_NEW:
            # New task
            try:
                task_id = self.task_list.push(message.content)
                return Message(MSG_TYPE_RESP, {'id': task_id})
            except KeyError:
                return Message(MSG_TYPE_ERROR,
                               {'error': 'Task id already exists'})

        elif message.type == MSG_TYPE_TASK_STATUS:
            # task status update
            status = message.content['status']
            # special case when task's status is TASK_STATUS_CANCELD, we dont'
            # want to change it's state.
            t = self.task_list.get(message.content['task_id'])
            if t.status & TASK_STATUS_CANCELED:
                status = t.status

            self.task_list.update(
                    t.id,
                    status=status,
                    output=message.content.get('output', None),
                    stop_datetime=message.content.get('stop_datetime', None),
            )
            return Message(MSG_TYPE_RESP, {'id': t.id})

        elif message.type == MSG_TYPE_TASK_LIST:
            # task list
            task_list = [t.__dict__ for task_id, t
                         in self.task_list.tasks.items()]
            return sorted(task_list, key=lambda k: k['start_datetime'])

        elif message.type == MSG_TYPE_TASK_ABORT:
            # task abortation
            t = Task(id=message.content['task_id'],
                     status=TASK_STATUS_ABORT)
            self.task_queue.put(t)

        elif message.type == MSG_TYPE_TASK_CANCEL:
            # task cancellation
            # first, we need to change its status
            self.task_list.update(
                    message.content['task_id'],
                    status=TASK_STATUS_CANCELED,
            )
            # send the cancelation order to WP
            t = Task(id=message.content['task_id'],
                     status=TASK_STATUS_CANCELED)
            self.task_queue.put(t)
        elif message.type == MSG_TYPE_CONTEXT:
            # context update
            if type(message.content) == dict:
                for k, v in message.content.items():
                    self.set_context(k, v)
                return Message(MSG_TYPE_RESP, self.get_context())
            else:
                return Message(MSG_TYPE_ERROR, 'Unvalid type')

        # TODO: handle other message types

    def start(self):
        # Queues
        self.task_queue = Queue()
        self.event_queue = Queue()
        # Instanciate WP
        self.worker_pool = WorkerPool(self.task_queue, self.event_queue)
        # Start WP as new process
        self.worker_pool.start()
        # Start Scheduler as new Process
        self.process = Process(target=self.run, args=())
        self.process.start()

    def stop(self):
        logger.debug("Abort remaining jobs if any")
        self.worker_pool.abort_jobs()
        logger.debug("Terminating WP process")
        self.worker_pool.process.terminate()
        logger.debug("Closing Listener")
        self.listener.close()
        logger.debug("Closing task_queue")
        self.task_queue.close()
        logger.debug("Closing event_queue")
        self.event_queue.close()
        del self.listener
        del self.worker_pool
        del self.task_queue
        del self.event_queue
        del self.task_list


class WorkerPool(object):

    def __init__(self, task_queue, event_queue):
        self.thread = None
        self.task_queue = task_queue
        self.event_queue = event_queue
        self.workers = {}

    def _abort_job(self, task_id):
        for workername in self.workers:
            for job in self.workers[workername]['pool']:
                if job['id'] == task_id:
                    logger.debug("Process pid=%s is going to be killed"
                                 % job['process'])
                    job['process'].terminate()
                    return True
        return False

    def _rm_task_worker_queue(self, task_id):
        for workername in self.workers:
            for t in self.workers[workername]['queue']:
                if t.id == task_id:
                    self.workers[workername]['queue'].remove(t)
                    logger.debug("Task %s removed from queue" % t.id)
                    return True
        return False

    def setup(self):
        global TM_WORKERS
        for worker in TM_WORKERS:
            self.add(worker)

    def add(self, worker):
        self.workers[worker['name']] = {
            'queue': deque(),
            'pool_size': worker['pool_size'],
            'module': worker['module'],
            'function': worker['function'],
            'pool': []
        }

    def serve1(self):
        # check running jobs state
        self.check_jobs()
        # start new jobs
        self.start_jobs()

        try:
            t = self.task_queue.get(timeout=0.1)
        except Empty:
            return

        if t.status & TASK_STATUS_SCHEDULED:
            logger.debug("Add Task %s to worker '%s' queue"
                         % (t.id, t.worker_name))
            self.workers[t.worker_name]['queue'].appendleft(t)
            # Update task status
            self.event_queue.put(
                Message(
                    MSG_TYPE_TASK_STATUS,
                    {
                        'task_id': t.id,
                        'status': TASK_STATUS_QUEUED,
                    }
                )
            )
        if t.status & TASK_STATUS_ABORT:
            self._abort_job(t.id)
        if t.status & TASK_STATUS_CANCELED:
            # Task cancellation includes 2 things:
            # - remove the task from workers queue if present (job not
            # yet running)
            # - abort running job executing the task if any

            # Looking up into workers jobs first, there is more chance
            # to find the task here.
            if not self._abort_job(t.id):
                # If not aborted, task has been queued
                self._rm_task_worker_queue(t.id)

    def run(self):
        self.setup()
        while True:
            try:
                self.serve1()
            except Exception as e:
                logger.exception(e)
            except KeyboardInterrupt:
                logger.error("KeyboardInterrupt")
                return

    def exec_worker(self, module, function, out, *args, **kws):
        # Function wrapper around worker function
        try:
            res = getattr(sys.modules[module], function)(*args, **kws)
            # Put function result into output queue as a Message
            out.put(Message(MSG_TYPE_RESP, res))
        except Exception as e:
            out.put(Message(MSG_TYPE_ERROR, e))
            logger.exception(e)
        except KeyboardInterrupt:
            logger.error("KeyboardInterrupt")

    def start_jobs(self):
        # Execute Tasks
        for name, worker in self.workers.items():
            while len(self.workers[name]['pool']) < worker['pool_size']:
                try:
                    t = worker['queue'].pop()
                    logger.debug("Startin new worker %s.%s"
                                 % (worker['module'], worker['function']))
                    # Queue used to get worker function return
                    out = Queue()
                    p = Process(
                            target=self.exec_worker,
                            args=(worker['module'], worker['function'], out),
                            kwargs=t.options,
                        )
                    p.start()
                    self.workers[name]['pool'].append(
                            {'id': t.id, 'process': p, 'out': out}
                    )
                    # Update task status
                    self.event_queue.put(
                        Message(
                            MSG_TYPE_TASK_STATUS,
                            {
                                'task_id': t.id,
                                'status': TASK_STATUS_DOING,
                            }
                        )
                    )
                except IndexError:
                    break

    def check_jobs(self):
        # Check jobs process state for each worker
        for name, worker in self.workers.items():
            for job in worker['pool']:
                if not job['process'].is_alive():
                    # Dead process case
                    logger.debug("Job %s is dead" % job['id'])
                    try:
                        # Fetch the message from job's output queue
                        message_out = job['out'].get(False)
                    except Empty:
                        message_out = None
                    logger.debug("Job output : %s" % message_out)
                    # Close job's output queue
                    job['out'].close()
                    # join the process
                    job['process'].join()

                    # Let's build the message we'll have to send to scheduler
                    # for the update of task's status.
                    task_stop_dt = datetime.utcnow()
                    if job['process'].exitcode == 0:
                        if message_out and \
                                message_out.type[0] == MSG_TYPE_RESP:
                            task_status = TASK_STATUS_DONE
                        else:
                            # when an exception is raised from the worker
                            # function
                            task_status = TASK_STATUS_FAILED
                    elif job['process'].exitcode < 0:
                        # process killed
                        task_status = TASK_STATUS_ABORTED
                    else:
                        task_status = TASK_STATUS_FAILED
                    task_output = None
                    if message_out:
                        task_output = message_out.content

                    # Update task status
                    self.event_queue.put(
                        Message(
                            MSG_TYPE_TASK_STATUS,
                            {
                                'task_id': job['id'],
                                'status': task_status,
                                'output': task_output,
                                'stop_datetime': task_stop_dt
                            }
                        )
                    )

                    # Finally, remove the job from the pool
                    self.workers[name]['pool'].remove(job)

    def start(self):
        self.process = Process(target=self.run, args=())
        self.process.start()

    def abort_jobs(self):
        # abort all running jobs
        for name, worker in self.workers.items():
            for job in worker['pool']:
                process = job.get('process')
                if process.is_alive():
                    process.terminate()
                    logger.debug("Job %s has been terminated" % job['id'])
                    # Close job's output queue
                    job['out'].close()
                    # join the process
                    process.join()
                    self.workers[name]['pool'].remove(job)


class WorkerSet(list):
    def register(self, pool_size=1):
        def register(f):
            f._tm_worker = make_worker_definition(f, pool_size)
            if f not in self:
                self.append(f)
            return f
        return register

    def schedule(self, id=None, redo_interval=None, **options):
        def register(f):
            if f not in self:
                self.append(f)
            f._tm_task = Task(
                id=id,
                options=options,
                redo_interval=redo_interval,
                worker_name=f.__name__,
            )
            return f
        return register

    def list_tasks(self):
        for function in self:
            task = getattr(function, '_tm_task', None)
            if task:
                yield task
