import json

import common
from .. import manager, servers, sources, users

class ServersHandler(common.AuthorizedHandler):
	def forbidden(self):
		return True

	def do_get(self):
		return 200, json.dumps(manager.server_list)

class ServerHandler(common.AuthorizedHandler):
	def __init__(self, request, response, groups):
		common.AuthorizedHandler.__init__(self, request, response, groups)
		self.server = manager.get(self.groups[0])

	def forbidden(self):
		return self.user.name in self.server.metadata.users

routes = { '/servers/': ServersHandler, '/servers/(' + servers.servers_allowed + ')(?:/(start|stop|reload|command|log|script))?': ServerHandler }
