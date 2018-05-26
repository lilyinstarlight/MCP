import os.path

import fooster.web.auth
import fooster.web.json
import fooster.web.page

import mcp.error

import mcp.model.user


class PageHandler(fooster.web.page.PageHandler):
    directory = os.path.dirname(__file__) + '/html'

class AuthHandler(fooster.web.auth.BasicAuthMixIn, fooster.web.json.JSONHandler):
    def auth_key(self, key):
        try:
            return mcp.model.user.check_key(key)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Key', 'MCP')

    def login(self, username, password):
        try:
            return mcp.model.user.check_user(username, password)
        except mcp.error.NoUserError:
            raise fooster.web.auth.AuthError('Basic', 'MCP')
