import datetime
import os
import shutil

from mcp import config, cron, manager

scheduler = None

def rotate_log(prefix, filename):
	if os.path.getsize(filename) > config.maxlogsize:
		shutil.copy(prefix + '/' + filename, prefix + '/log/' + datetime.strftime('%Y-%m-%d_%H-%M') + '.' + filename)
		with open(filename, 'w') as file:
			pass

def rotate():
	for server in manager.server_list:
		rotate_log(server.prefix, 'server.log')
		rotate_log(server.prefix, 'error.log')
		rotate_log(server.prefix, 'script-error.log')

def start():
	global scheduler

	scheduler = cron.Scheduler()
	scheduler.add(cron.Job(rotate, minute=0))
	scheduler.start()

def stop():
	global scheduler

	scheduler.stop()
	scheduler = None
