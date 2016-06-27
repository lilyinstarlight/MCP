import logging
import threading
import time

name = 'cron.py'
version = '0.3'


class Field(object):
    def __init__(self, param):
        self.param = param

    def __repr__(self):
        return 'cron.Field(' + repr(self.param) + ')'


class All(Field):
    def __init__(self):
        pass

    def __eq__(self, value):
        return True

    def __repr__(self):
        return 'cron.All()'


class Every(Field):
    def __eq__(self, value):
        return value % self.param == 0

    def __repr__(self):
        return 'cron.Every(' + repr(self.param) + ')'


class Int(Field):
    def __eq__(self, value):
        return value == self.param

    def __repr__(self):
        return repr(self.param)


class List(Field):
    def __eq__(self, value):
        return value in self.param

    def __repr__(self):
        return repr(self.param)


def create_field(value):
    if isinstance(value, Field):
        return value
    elif isinstance(value, int):
        return Int(value)
    elif isinstance(value, list):
        return List(value)
    else:
        raise TypeError()


class Job(object):
    def __init__(self, function, args=(), kwargs={}, name=None, minute=All(), hour=All(), day=All(), month=All(), weekday=All()):
        self.function = function
        self.args = args
        self.kwargs = kwargs

        if name:
            self.name = name
        else:
            self.name = self.function.__name__

        self.minute = create_field(minute)
        self.hour = create_field(hour)
        self.day = create_field(day)
        self.month = create_field(month)
        self.weekday = create_field(weekday)

    def __str__(self):
        return '<cron.Job \'' + self.name + '\'>'

    def __repr__(self):
        return 'cron.Job(' + repr(self.function) + ', args=' + repr(self.args) + ', kwargs=' + repr(self.kwargs) + ', name=' + repr(self.name) + ', minute=' + repr(self.minute) + ', hour=' + repr(self.hour) + ', day=' + repr(self.day) + ', month=' + repr(self.month) + ', weekday=' + repr(self.weekday) + ')'

    def should_run(self, time):
        return time.tm_min == self.minute and time.tm_hour == self.hour and time.tm_mday == self.day and time.tm_mon == self.month and time.tm_wday == self.weekday

    def run(self):
        self.function(*self.args, **self.kwargs)


class Scheduler(object):
    def __init__(self, log=logging.getLogger(__name__), time=time.localtime):
        self.log = log
        self.time = time

        self.jobs = []
        self.jobs_lock = threading.Lock()

        self.running = False
        self.thread = None

    def __repr__(self):
        return 'cron.Scheduler(log=' + repr(self.log) + ', time=' + repr(self.time) + ')'

    def add(self, job):
        with self.jobs_lock:
            self.jobs.append(job)

    def remove(self, job):
        with self.jobs_lock:
            self.jobs.remove(job)

    def start(self):
        if self.is_running():
            return

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        self.log.info('Scheduler running')

    def stop(self):
        if not self.is_running():
            return

        self.running = False
        self.thread.join()
        self.thread = None

        self.log.info('Scheduler stopped')

    def is_running(self):
        return bool(self.thread and self.thread.is_alive())

    def run(self):
        while self.running:
            # get times
            ctime = time.time()
            ltime = self.time(ctime)

            # get sleep target to run on the minute
            sleep_target = ctime + 60 - ltime.tm_sec

            # copy jobs to prevent iterating over a mutating list
            with self.jobs_lock:
                jobs = self.jobs.copy()

            # go through each job and run it if necessary
            for job in jobs:
                try:
                    if job.should_run(ltime):
                        job.run()
                except:
                    self.log.exception('Caught exception on job "' + job.name + '"')

            # get new time after running jobs
            ctime = time.time()

            try:
                # wait until sleep target
                time.sleep(sleep_target - ctime)
            except ValueError:
                # if sleep target is missed, don't bother sleeping
                pass
