import sys
import time

from armaadmin import config

log = None
cmdlog = None
httplog = None

def init():
	global log
	global cmdlog
	global httplog

	if config.log:
		os.makedirs(os.path.dirname(config.log), exist_ok=True)
		log = open(config.log, 'a', 1)

	if config.cmdlog:
		os.makedirs(os.path.dirname(config.cmdlog), exist_ok=True)
		cmdlog = open(config.cmdlog, 'a', 1)

	if config.httplog:
		os.makedirs(os.path.dirname(config.httplog), exist_ok=True)
		httplog = open(config.httplog, 'a', 1)


def close():
	global log
	global cmdlog
	global httplog

	if log:
		log.close()
		log = None

	if cmdlog:
		cmdlog.close()
		cmdlog = None

	if httplog:
		httplog.close()
		httplog = None

def write(format, *args):
	if log:
		log.write('[%s] %s\n' % (time.strftime('%Y/%m/%d %H:%M:%S'), format % args))

def info(format, *args):
	write('INFO: ' + format, *args)

def warn(format, *args):
	write('WARNING: ' + format, *args)

def error(format, *args):
	write('ERROR: ' + format, *args)

def exception(msg):
	type, value, traceback = sys.exc_info()
	error('Caught %s while %s: %s', type.__name__, msg, value)
