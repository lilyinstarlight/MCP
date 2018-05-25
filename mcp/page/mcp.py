import os

import fooster.web.file

import mcp.common.http


class IndexHandler(mcp.common.http.PageHandler):
    page = 'index.html'


class SetupHandler(mcp.common.http.PageHandler):
    page = 'setup.html'


class ServerHandler(mcp.common.http.PageHandler):
    page = 'server.html'


class AdminHandler(mcp.common.http.PageHandler):
    page = 'admin.html'


class UserHandler(mcp.common.http.PageHandler):
    page = 'user.html'


class LoginHandler(mcp.common.http.PageHandler):
    page = 'login.html'


routes = {'/': IndexHandler, '/setup': SetupHandler, '/server': ServerHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler}

routes.update(fooster.web.file.new(os.path.dirname(__file__) + '/res', '/res'))
