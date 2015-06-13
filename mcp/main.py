import signal

from mcp import name, version
from mcp import interface, log, manager, rotate

log.mcplog.info(name + ' ' + version + ' starting...')

#Start everything
manager.start()
rotate.start()
interface.start()

#Cleanup (exit) function
def exit():
	interface.stop()
	rotate.stop()
	manager.stop()

#Use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
	signal.signal(sig, exit)
