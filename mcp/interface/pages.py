from mcp.interface import common

class IndexHandler(common.PageHandler):
	page = 'index.html'

class ServerHandler(common.PageHandler):
	page = 'server.html'

class AdminHandler(common.PageHandler):
	page = 'admin.html'

class UserHandler(common.PageHandler):
	page = 'user.html'

class LoginHandler(common.PageHandler):
	page = 'login.html'

routes = { '/': IndexHandler, '/server': ServerHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler }
