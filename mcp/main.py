import argparse
import logging
import multiprocessing
import os
import os.path
import shutil
import signal
import sys

import fooster.web


import mcp.config


parser = argparse.ArgumentParser(description='start a multi-server management framework for Armagetron Advanced')
parser.add_argument('-a', '--address', dest='address', help='address to bind')
parser.add_argument('-p', '--port', type=int, dest='port', help='port to bind')
parser.add_argument('-t', '--template', dest='template', help='template directory to use')
parser.add_argument('-l', '--log', dest='log', help='log directory to use')
parser.add_argument('--db', '--database', dest='database', help='database directory to use')
parser.add_argument('--prefix', dest='prefix', help='prefix directory to use')
parser.add_argument('--sources', dest='sources', help='sources directory to use')
parser.add_argument('--config', dest='config', help='config directory to use')
parser.add_argument('--scripting', dest='scripting', help='scripting directory to use')
parser.add_argument('--tmp', dest='tmp', help='tmp directory to use')
parser.add_argument('--chroot', action='store_true', dest='chroot', help='whether to chroot scripts')

args = parser.parse_args()

if args.address:
    mcp.config.addr = (args.address, mcp.config.addr[1])

if args.port:
    mcp.config.addr = (mcp.config.addr[0], args.port)

if args.template:
    config.template = args.template

if args.log:
    if args.log == 'none':
        mcp.config.log = None
        mcp.config.cmdlog = None
        mcp.config.httpdlog = None
        mcp.config.accesslog = None
    else:
        mcp.config.log = os.path.join(args.log, 'manager.log')
        mcp.config.cmdlog = os.path.join(args.log, 'command.log')
        mcp.config.httplog = os.path.join(args.log, 'httpd.log')
        mcp.config.accesslog = os.path.join(args.log, 'access.log')

if args.database:
    mcp.config.database = os.path.abspath(args.database)

if args.prefix:
    mcp.config.prefix = os.path.abspath(args.prefix)

if args.sources:
    mcp.config.sources = os.path.abspath(args.sources)

if args.config:
    mcp.config.config = os.path.abspath(args.config)

if args.scripting:
    mcp.config.scripting = os.path.abspath(args.scripting)

if args.tmp:
    mcp.config.tmp = os.path.abspath(args.tmp)

if args.chroot:
    mcp.config.chroot = args.chroot


if mcp.config.log:
    logging.getLogger('mcp').addHandler(logging.FileHandler(mcp.config.log))


if mcp.config.cmdlog:
    logging.getLogger('cmd').addHandler(logging.FileHandler(mcp.config.cmdlog))


if mcp.config.httpdlog:
    httpdlog_handler = logging.FileHandler(mcp.config.httpdlog)
    httpdlog_handler.setFormatter(fooster.web.HTTPLogFormatter())

    logging.getLogger('web').addHandler(httpdlog_handler)


if mcp.config.accesslog:
    logging.getLogger('http').addHandler(logging.FileHandler(mcp.config.accesslog))


from mcp import name, version

import mcp.initial

import mcp.common.daemon

import mcp.service.http
import mcp.service.manager
import mcp.service.rotate
import mcp.service.update

log = logging.getLogger('mcp')

log.info(name + ' ' + version + ' starting...')

# fix multiprocessing ctrl+c
signal.signal(signal.SIGINT, signal.SIG_IGN)

# check for starting files
mcp.initial.check()

# fill in daemon details
mcp.common.daemon.pid = os.getpid()
mcp.common.daemon.sync = multiprocessing.Manager()

# start everything
mcp.service.manager.start()
mcp.service.rotate.start()
mcp.service.update.start()
mcp.service.http.start()

# cleanup function
def exit(signum, frame):
    mcp.service.http.stop()

# restart function
def restart(signum, frame):
    mcp.service.manager.stop()
    mcp.service.manager.start()

# use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
    signal.signal(sig, exit)

# use SIGUSR1 for restart
signal.signal(signal.SIGUSR1, restart)

# wait for http to finish
mcp.service.http.join()

# stop background services
mcp.service.update.stop()
mcp.service.rotate.stop()
mcp.service.manager.stop()
