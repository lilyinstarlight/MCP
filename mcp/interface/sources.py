import json

from mcp import sources
from mcp.interface import common

class SourcesHandler(common.AuthorizedHandler):
	def forbidden(self):
		return False

	def do_get(self):
		return 200, json.dumps(list(iter(sources.source_db)))

class SourceHandler(common.AuthorizedHandler):
	def __init__(self, request, response, groups):
		common.AuthorizedHandler.__init__(self, request, response, groups)
		self.source = sources.get(self.groups[0])

class SourceInfoHandler(SourceHandler):
	def do_get(self):
		return 200, json.dumps({'name': self.source.source, 'url': self.source.url, 'revision': self.source.revision})

	def add(self, url):
		if not self.user.admin:
			self.forbidden_error()

		sources.add(self.groups[0], url)

	def modify(self):
		if not self.user.admin:
			self.forbidden_error()

		sources.update(self.source.source)

	def do_put(self):
		info = json.loads(self.request.body)

		if not self.source:
			self.add(info['url'])

			return 201, ''
		else:
			self.modify()

			return 204, ''

	def do_patch(self):
		if not self.source:
			raise web.HTTPError(404)

		info = json.loads(self.request.body)

		self.modify()

		return 204, ''

	def do_delete(self):
		if not self.user.admin:
			self.forbidden_error()

		if not self.source:
			raise web.HTTPError(404)

		sources.remove(self.source.source)

		return 204, ''

sources_base = '/sources/'
source_base = sources_base + '(' + sources.sources_allowed + ')'

routes = {sources_base: SourcesHandler, source_base: SourceInfoHandler}
