import signal

from mcp import name, version

from mcp.common import log
from mcp.service import http, manager, rotate

log.mcplog.info(name + ' ' + version + ' starting...')

# start everything
manager.start()
rotate.start()
http.start()

# cleanup function
def exit():
    http.stop()
    rotate.stop()
    manager.stop()

# use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
    signal.signal(sig, exit)
