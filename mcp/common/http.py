import os.path

import fooster.web.auth
import fooster.web.json
import fooster.web.page
import fooster.web.query

import mcp.error

import mcp.model.user


class PageHandler(fooster.web.page.PageHandler):
    directory = os.path.dirname(__file__) + '/html'

class PlainAuthHandler(fooster.web.auth.BasicAuthMixIn, fooster.web.query.QueryMixIn, fooster.web.HTTPHandler):
    group = 1

    def login(self, username, password):
        try:
            return mcp.model.user.check_user(username, password)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Basic', 'MCP')

    def auth_key(self, key):
        try:
            return mcp.model.user.check_key(key)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Key', 'MCP')

    def auth_token(self, token):
        try:
            return mcp.model.user.check_token(token)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Token', 'MCP')

    def forbidden(self):
        return not self.auth.active

class AuthHandler(fooster.web.json.JSONMixIn, PlainAuthHandler):
    pass
