import time

import armaadmin.interface
import armaadmin.manager
import armaadmin.web

for server in manager.servers.values():
	if server.exists():
		server.start()
		time.sleep(3)

http = web.create(interface.routes)

while True:
	manager.poll()
	time.sleep(3)

web.destroy(http)
