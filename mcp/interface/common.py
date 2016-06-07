import base64
import os

from mcp import users
from mcp.interface import web

class AuthorizedHandler(web.HTTPHandler):
    auth_types = ['Basic', 'Key']
    realm = 'unknown'

    def __init__(self, request, response, groups):
        web.HTTPHandler.__init__(self, request, response, groups)
        self.user = None

    def respond(self):
        auth = self.request.headers.get('Authorization')

        if not auth:
            self.auth_error()

        try:
            self.auth_type, self.auth_string = auth.split(' ', 1)
        # ignore bad Authorization headers
        except:
            self.auth_error()

        if not self.auth_type in self.auth_types:
            self.auth_error()

        if not self.authorized():
            self.auth_error()

        if (self.forbidden() or not self.user.active) and not self.user.admin:
            self.forbidden_error()

        web.HTTPHandler.respond(self)

    def auth_error(self):
        auth_headers = web.HTTPHeaders()
        auth_headers.set('WWW-Authenticate', ','.join(self.auth_types) + ' realm="' + self.realm + '"')
        raise web.HTTPError(401, headers=auth_headers)

    def forbidden_error(self):
        raise web.HTTPError(403)

    def authorized(self):
        try:
            if self.auth_type == 'Basic':
                username, password = base64.b64decode(self.auth_string).decode('utf-8').split(':', 1)
                self.user = users.check_user(username, password)
            elif self.auth_type == 'Key':
                self.user = users.check_key(self.auth_string)
        except:
            return False

        return self.user != None

    def forbidden(self):
        return False

class PageHandler(web.HTTPHandler):
    page = 'index.html'

    def do_get(self):
        self.response.headers.set('Content-Type', 'text/html')
        return 200, open(os.path.dirname(__file__) + '/html/' + self.page, 'r')
