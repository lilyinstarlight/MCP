import sys
import time

from armaadmin import config
from armaadmin import name, version

log = None

def init():
	global log

	if config.log:
		log = open(config.log, 'a', 1)
		write(name + ' ' + version + ' started')

def close():
	if log:
		log.close()
		log = None

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
