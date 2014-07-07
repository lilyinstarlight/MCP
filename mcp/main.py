import signal
import time

import config, interface, log, manager, web
from . import name, version

running = True

def sigterm(signum, frame):
	global running
	running = False

signal.signal(signal.SIGTERM, sigterm)

log.init()
web.init(config.address, config.port, interface.routes, log.httplog)

log.info(name + ' ' + version + ' started')

for server in manager.servers.values():
	if server.exists():
		server.start()
		time.sleep(3)

while running:
	manager.poll()
	time.sleep(3)

web.destroy()
log.close()
