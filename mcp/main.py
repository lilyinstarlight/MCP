import signal

from . import interface, log, manager

from . import name, version

log.mcplog.info(name + ' ' + version + ' starting...')

#Start everything
manager.start()
interface.start()

#Cleanup (exit) function
def exit():
	interface.stop()
	manager.stop()

#Set the function to both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
	signal.signal(sig, exit)
