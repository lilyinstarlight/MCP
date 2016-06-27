import json

from mcp.model import user
from mcp.api import handler
from mcp.lib import web

class UsersHandler(common.AuthorizedHandler):
    def forbidden(self):
        return True

    def do_get(self):
        return 200, json.dumps(list(iter(users.user_db)))

class UserHandler(common.AuthorizedHandler):
    def __init__(self, request, response, groups):
        common.AuthorizedHandler.__init__(self, request, response, groups)
        self.userentry = users.get(self.groups[0])

    def forbidden(self):
        return not self.userentry or self.user.name != self.userentry.name

class UserInfoHandler(UserHandler):
    def do_get(self):
        if not self.userentry:
            raise web.HTTPError(404)

        return 200, json.dumps({'username': self.userentry.username, 'key': self.userentry.key, 'admin': self.userentry.admin, 'active': self.userentry.active, 'servers': self.userentry.servers})

    def add(self, password, key, admin, active, servers):
        if not self.user.admin:
            self.forbidden_error()

        users.add(self.groups[0], password, key, admin, active, servers)

    def modify(self, password, key, admin, active, servers):
        if (admin != None or active != None or servers != None) and not self.user.admin:
            self.forbidden_error()

        users.modify(self.userentry.username, password, key, admin, active, servers)

    def do_put(self):
        info = json.loads(self.request.body)

        if not self.userentry:
            self.add(info['password'], info['key'], info['admin'], info['active'], info['servers'])

            return 201, ''
        else:
            self.modify(info['password'], info['key'], info['admin'], info['active'], info['servers'])

            return 204, ''

    def do_patch(self):
        if not self.userentry:
            raise web.HTTPError(404)

        info = json.loads(self.request.body)

        self.modify(info.get('password'), info.get('key'), info.get('admin'), info.get('active'), info.get('servers'))

        return 204, ''

    def do_delete(self):
        if not self.user.admin:
            self.forbidden_error()

        if not self.userentry:
            raise web.HTTPError(404)

        users.remove(self.userentry.username)

        return 204, ''

users_base = '/users/'
user_base = users_base + '(' + users.users_allowed + ')'

routes = {users_base: UsersHandler, user_base: UserInfoHandler}
