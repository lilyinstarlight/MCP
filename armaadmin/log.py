import sys
import time

from armaadmin import config

log = None
cmdlog = None

def init():
	global log
	global cmdlog

	if config.log:
		log = open(config.log, 'a', 1)

	if config.cmdlog:
		cmdlog = open(config.cmdlog, 'a', 1)

def close():
	global log
	global cmdlog

	if log:
		log.close()
		log = None

	if cmdlog:
		cmdlog.close()
		cmdlog = None

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
