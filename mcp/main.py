import signal

from mcp import name, version
from mcp import interface, log, manager

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
