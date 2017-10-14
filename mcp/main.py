import logging
import signal


if config.log:
    logging.getLogger('mcp').addHandler(logging.FileHandler(config.log))


if config.cmdlog:
    logging.getLogger('cmd').addHandler(logging.FileHandler(config.cmdlog))


if config.httpdlog:
    httpdlog_handler = logging.FileHandler(config.httpdlog)
    httpdlog_handler.setFormatter(web.HTTPLogFormatter())

    logging.getLogger('http').addHandler(httpdlog_handler)


if config.accesslog:
    logging.getLogger('web').addHandler(logging.FileHandler(config.accesslog))


from mcp import name, version

from mcp.service import http, manager, rotate

log = logging.getLogger('mcp')

log.info(name + ' ' + version + ' starting...')

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
