import os

import fooster.web.file

import mcp.config

import mcp.common.http


class IndexHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'index.html'


class SetupHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'setup.html'


class ServerHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'server.html'


class AdminHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'admin.html'


class UserHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'user.html'


class LoginHandler(mcp.common.http.PageHandler):
    directory = mcp.config.template
    page = 'login.html'


routes = {'/': IndexHandler, '/setup': SetupHandler, '/server': ServerHandler, '/admin': AdminHandler, '/user': UserHandler, '/login': LoginHandler}

routes.update(fooster.web.file.new(mcp.config.template + '/res', '/res'))
