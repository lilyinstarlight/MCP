from mcp.interface import common

class IndexHandler(common.PageHandler):
    page = 'index.html'

class SetupHandler(common.PageHandler):
    page = 'setup.html'

class ServerHandler(common.PageHandler):
    page = 'server.html'

class AdminHandler(common.PageHandler):
    page = 'admin.html'

class UserHandler(common.PageHandler):
    page = 'user.html'

class LoginHandler(common.PageHandler):
    page = 'login.html'

routes = {'/': IndexHandler, '/setup': SetupHandler, '/server': ServerHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler}

routes.update(file.new(os.path.dirname(__file__) + '/res', '/res'))
