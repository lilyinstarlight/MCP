import base64
import os

import web
from .. import users

class AuthorizedHandler(web.HTTPHandler):
	auth = [ 'Basic', 'Key' ]
	realm = 'unknown'

	def respond(self):
		auth_header = self.request.headers.get('Authorization')

		if not auth_header:
			return unauthorized()

		try:
			self.auth_type, self.auth_string = auth_header.split(' ', 1)
		#Ignore bad Authorization headers
		except:
			return unauthorized()

		if not self.auth_type in self.auth:
			return unauthorized()

		web.HTTPHandler.respond(self)

	def unauthorized(self):
		raise web.HTTPError(401, headers=web.HTTPHeaders().set('WWW-Authenticate', ','.join(self.auth) + ' realm="' + self.realm + '"'))

class PageHandler(web.HTTPHandler):
	page = 'index.html'

	def do_get(self):
		with open(os.path.dirname(__file__) + '/html/' + self.page, 'r') as file:
			self.response.headers.set('Content-Type', 'text/html')
			return 200, file
