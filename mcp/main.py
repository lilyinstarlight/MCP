import signal

from mcp import name, version
from mcp import interface, log, manager, rotate

log.mcplog.info(name + ' ' + version + ' starting...')

# start everything
manager.start()
rotate.start()
interface.start()

# cleanup (exit) function
def exit():
    interface.stop()
    rotate.stop()
    manager.stop()

# use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
    signal.signal(sig, exit)
