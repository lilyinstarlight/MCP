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

def write(format, *args):
	if log:
		log.write('[%s] %s\n' % (self.log_date_time_string(), format % args))

def warn(format, *args):
	write('Warning: ' + format, args)

def error(msg):
	write('Error: ' + format, args)
