import time

from armaadmin import interface, manager, web

for server in manager.servers.values():
	if server.exists():
		server.start()
		time.sleep(3)

web.init(interface.routes)

while True:
	manager.poll()
	time.sleep(3)

web.destroy()
