import argparse
import logging
import signal


from mcp import config


parser = argparse.ArgumentParser(description='start a multi-server management framework for Armagetron Advanced')
parser.add_argument('-a', '--address', dest='address', help='address to bind')
parser.add_argument('-p', '--port', type=int, dest='port', help='port to bind')
parser.add_argument('-l', '--log', dest='log', help='log directory to use')
parser.add_argument('--db', '--database', dest='database', help='database directory to use')
parser.add_argument('--prefix', dest='prefix', help='prefix directory to use')
parser.add_argument('--sources', dest='sources', help='sources directory to use')
parser.add_argument('--config', dest='config', help='config directory to use')
parser.add_argument('--scripting', dest='scripting', help='scripting directory to use')
parser.add_argument('--tmp', dest='tmp', help='tmp directory to use')

args = parser.parse_args()

if args.address:
    config.addr = (args.address, config.addr[1])

if args.port:
    config.addr = (config.addr[0], args.port)

if args.log:
    if args.log == 'none':
        config.log = None
        config.cmdlog = None
        config.httpdlog = None
        config.accesslog = None
    else:
        config.log = args.log + '/manager.log'
        config.cmdlog = args.log + '/command.log'
        config.httpdlog = args.log + '/httpd.log'
        config.accesslog = args.log + '/access.log'

if args.database:
    config.database = args.database

if args.prefix:
    config.prefix = args.prefix

if args.sources:
    config.sources = args.sources

if args.config:
    config.config = args.config

if args.scripting:
    config.scripting = args.scripting

if args.tmp:
    config.tmp = args.tmp


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
