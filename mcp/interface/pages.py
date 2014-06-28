import common

class RootHandler(common.PageHandler):
	page = 'index.html'

class AdminHandler(common.PageHandler):
	page = 'admin.html'

class UserHandler(common.PageHandler):
	page = 'user.html'

class LoginHandler(common.PageHandler):
	page = 'login.html'

routes = { '/': RootHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler }
