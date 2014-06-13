import common

class RootHandler(common.AuthPageHandler):
	page = 'index.html'

class AdminHandler(common.AuthPageHandler):
	page = 'admin.html'

class UserHandler(common.AuthPageHandler):
	page = 'user.html'

class LoginHandler(common.PageHandler):
	page = 'login.html'

routes = { '/': RootHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler }
