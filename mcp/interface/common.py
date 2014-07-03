import base64
import os

import web
from .. import users

class AuthorizedHandler(web.HTTPHandler):
	auth_types = [ 'Basic', 'Key' ]
	realm = 'unknown'

	def respond(self):
		auth = self.request.headers.get('Authorization')

		if not auth:
			auth_error()

		try:
			self.auth_type, self.auth_string = auth.split(' ', 1)
		#Ignore bad Authorization headers
		except:
			auth_error()

		if not self.auth_type in self.auth_types:
			auth_error()

		if not authorized():
			auth_error()

		if not user.admin and forbidden():
			forbidden_error()

		web.HTTPHandler.respond(self)

	def auth_error(self):
		raise web.HTTPError(401, headers=web.HTTPHeaders().set('WWW-Authenticate', ','.join(self.auth_types) + ' realm="' + self.realm + '"'))

	def forbidden_error(self):
		raise web.HTTPError(403)

	def authorized(self):
		self.user = None

		try:
			if self.auth_type == 'Basic':
				username, password = base64.b64decode(self.auth_string).decode('utf-8').split(':', 1)
				self.user = users.check_user(username, password)
			elif self.auth_type == 'Key':
				self.user = users.check_key(self.auth_string)
		except:
			auth_error()

		return self.user != None

	def forbidden(self):
		return False

class PageHandler(web.HTTPHandler):
	page = 'index.html'

	def do_get(self):
		with open(os.path.dirname(__file__) + '/html/' + self.page, 'r') as file:
			self.response.headers.set('Content-Type', 'text/html')
			return 200, file
