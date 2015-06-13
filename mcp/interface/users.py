import json

from mcp import users
from mcp.interface import common

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
		return self.user.name != self.userentry.name

class UserInfoHandler(UserHandler):
	def do_get(self):
		return 200, json.dumps({'name': self.userentry.name, 'key': self.userentry.key, 'admin': self.userentry.admin, 'active': self.userentry.active, 'servers': self.userentry.servers})

users_base = '/users/'
user_base = users_base + '(' + users.users_allowed + ')'

routes = {users_base: UsersHandler, user_base: UserInfoHandler}
