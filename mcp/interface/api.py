import json

from mcp import manager, servers, sources, users
from mcp.interface import common

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

class ServerInfoHandler(ServerHandler):
	def do_get(self):
		return 200, json.dumps({'name': self.server.name, 'running': self.server.is_running(), 'source': self.server.metadata.source, 'revision': self.server.metadata.revision, 'port': self.server.metadata.port, 'autostart': self.server.metadata.autostart, 'users': self.server.metadata.users})

class ServerLogHandler(ServerHandler):
	def do_get(self):
		return 200, open(self.server.prefix + '/server.log', 'r')

class ServerConfigHandler(ScriptHandler):
	def do_put(self):
		with open(self.server.prefix + '/config/settings_custom.cfg', 'w') as file:
			file.write(self.request.body);

		self.server.reload()

		return 204, ''

class ServerErrorLogHandler(ServerHandler):
	def do_get(self):
		return 200, open(self.server.prefix + '/error.log', 'r')

class ServerActionHandler(ServerHandler):
	def do_post(self):
		action = self.groups[1]

		if action == 'start':
			self.server.start()
		elif action == 'stop':
			self.server.stop()
		elif action == 'restart':
			self.server.stop()
			self.server.start()
		elif action == 'reload':
			self.server.reload()
		elif action == 'command':
			self.server.send_command(self.request.body)

		return 204, ''

class ScriptHandler(ServerHandler):
	def __init__(self, request, response, groups):
		ServerHandler.__init__(self, request, response, groups)
		self.script = self.server.script

class ScriptInfoHandler(ScriptHandler):
	def do_get(self):
		return 200, json.dumps({'name': self.server.name, 'running': self.script.is_running()})

class ScriptSourceHandler(ScriptHandler):
	def do_put(self):
		with open(self.server.prefix + '/scripts/script.py', 'w') as file:
			file.write(self.request.body);

		self.script.stop()
		self.script.start()

		return 204, ''

class ScriptErrorLogHandler(ScriptHandler):
	def do_get(self):
		return 200, open(self.server.prefix + '/script-error.log', 'r')

class ScriptActionHandler(ScriptHandler):
	def do_post(self):
		action = self.groups[1]

		if action == 'start':
			self.script.start()
		elif action == 'stop':
			self.script.stop()
		elif action == 'restart':
			self.script.stop()
			self.script.start()

		return 204, ''

servers_base = '/servers/'
server_base = servers_base + '(' + servers.servers_allowed + ')'
script_base = server_base + '/script'
routes = {servers_base: ServersHandler, server_base: ServerInfoHandler, server_base + '/config': ServerConfigHandler, server_base + '/log': ServerLogHandler, server_base + '/error': ServerErrorLogHandler, server_base + '/(start|stop|restart|reload|command)': ServerActionHandler, script_base: ScriptInfoHandler, script_base + '/source': ScriptSourceHandler, script_base + '/error': ScriptErrorLogHandler, script_base + '/(start|stop|restart)': ScriptActionHandler}
