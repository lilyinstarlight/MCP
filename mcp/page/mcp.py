import os

from fooster import web


class PageHandler(web.page.PageHandler):
    directory = os.path.dirname(__file__) + '/html'


class IndexHandler(PageHandler):
    page = 'index.html'


class SetupHandler(PageHandler):
    page = 'setup.html'


class ServerHandler(PageHandler):
    page = 'server.html'


class AdminHandler(PageHandler):
    page = 'admin.html'


class UserHandler(PageHandler):
    page = 'user.html'


class LoginHandler(PageHandler):
    page = 'login.html'


routes = {'/': IndexHandler, '/setup': SetupHandler, '/server': ServerHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler}

routes.update(file.new(os.path.dirname(__file__) + '/res', '/res'))
