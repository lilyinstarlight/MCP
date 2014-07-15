import sys
import threading
import time

name = 'cron.py'
version = '0.1'

class Field(object):
	def __init__(self, param):
		self.param = param

class All(Field):
	def __init__(self):
		pass

	def __eq__(self, value):
		return True

class Every(Field):
	def __eq__(self, value):
		return value % self.param == 0

class Int(Field):
	def __eq__(self, value):
		return value == self.param

class List(Field):
	def __eq__(self, value):
		return value in self.param

def create_field(value):
	if isinstance(value, Field):
		return value
	elif isinstance(value, int):
		return Int(value)
	elif isinstance(value, list):
		return List(value)
	else:
		raise TypeError()

class Log(object):
	def __init__(self, log):
		if log:
			os.makedirs(os.path.dirname(log), exist_ok=True)
			self.log = open(log, 'a', 1)
		else:
			self.log = sys.stderr

	def timestamp(self):
		return time.strftime('[%d/%b/%Y:%H:%M:%S %z]')

	def write(self, string):
		self.log.write(string)

	def message(self, message):
		self.write(self.timestamp() + ' ' + message + '\n')

	def info(self, message):
		self.message('INFO: ' + message)

	def warn(self, message):
		self.message('WARN: ' + message)

	def error(self, message):
		self.message('ERROR: ' + message)

	def exception(self):
		self.error('Caught exception:\n\t' + traceback.format_exc().replace('\n', '\n\t'))

class Job(object):
	def __init__(self, function, args=[], kwargs={}, minute=All(), hour=All(), day=All(), month=All(), weekday=All()):
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.minute = create_field(minute)
		self.hour = create_field(hour)
		self.day = create_field(day)
		self.month = create_field(month)
		self.weekday = create_field(weekday)

	def should_run(self, time):
		return time.tm_min == self.minute and time.tm_hour == self.hour and time.tm_mday == self.day and time.tm_mon == self.month and time.tm_wday == self.weekday

	def run(self):
		self.function(*self.args, **self.kwargs)

class Scheduler(object):
	def __init__(self, log=Log(None)):
		self.log = log

		self.jobs = []

		self.running = False
		self.thread = None

	def add(self, job):
		self.jobs.append(job)

	def remove(self, ob):
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
		return self.thread and self.thread.is_alive()

	def run(self):
		while self.running:
			#Get times
			ctime = time.time()
			ltime = time.localtime(ctime)

			#Get sleep target to run on the minute
			sleep_target = ctime + 60 - ltime.tm_sec

			#Go through each job and run it if necessary
			for job in self.jobs:
				try:
					if job.should_run(ltime):
						job.run()
				except:
					self.log.exception()

			#Get new time after running jobs
			ctime = time.time()

			#Wait until sleep target
			time.sleep(sleep_target - ctime)
