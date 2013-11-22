import signal
import time

from armaadmin import interface, log, manager, web

running = True

def sigterm(signum, frame):
	global running
	running = False

signal.signal(signal.SIGTERM, sigterm)

log.init()
web.init(interface.routes)

for server in manager.servers.values():
	if server.exists():
		server.start()
		time.sleep(3)

while running:
	manager.poll()
	time.sleep(3)

web.destroy()
log.close()
