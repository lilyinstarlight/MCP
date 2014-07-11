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

def Int(Field):
	def __eq__(self, value):
		return value == self.param

def List(Field):
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
	def __init__(self):
		self.jobs = []
		self.thread = threading.Thread(target=self.run)

	def add(self, job):
		self.jobs.append(job)

	def remove(self, ob):
		self.jobs.remove(job)

	def start(self):
		self.running = True
		self.thread.start()

	def stop(self):
		self.running = False

	def run(self):
		while self.running:
			#Get times
			ctime = time.time()
			ltime = time.localtime(ctime)

			#Get sleep target to run on the minute
			sleep_target = ctime + 60 - ltime.tm_sec

			#Go through each job and run it if necessary
			for job in self.jobs:
				if job.should_run(ltime):
					job.run()

			#Get new time after running jobs
			ctime = time.time()

			#Wait until sleep target
			time.sleep(sleep_target - ctime)
