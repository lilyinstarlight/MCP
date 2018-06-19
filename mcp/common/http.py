import base64
import os.path

import fooster.web.auth
import fooster.web.json
import fooster.web.page
import fooster.web.query

import mcp.error

import mcp.model.user


class PageHandler(fooster.web.page.PageHandler):
    directory = os.path.join(os.path.dirname(__file__), 'html')

class PlainHandler(fooster.web.query.QueryMixIn, fooster.web.HTTPHandler):
    pass

class PlainAuthHandler(fooster.web.auth.BasicAuthMixIn, PlainHandler):
    def login(self, username, password):
        try:
            return mcp.model.user.check_user(username, password)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Basic', 'MCP')

    def auth_login(self, userpass):
        try:
            username, password = base64.b64decode(userpass).decode().split(':', 1)

            return mcp.model.user.check_user(username, password)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Login', 'MCP')

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
