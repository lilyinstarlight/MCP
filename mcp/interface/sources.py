import json

from mcp import sources
from mcp.interface import common

class SourcesHandler(common.AuthorizedHandler):
	def forbidden(self):
		return True

	def do_get(self):
		return 200, json.dumps(list(iter(sources.source_db)))

class SourceHandler(common.AuthorizedHandler):
	def __init__(self, request, response, groups):
		common.AuthorizedHandler.__init__(self, request, response, groups)
		self.source = sources.get(self.groups[0])

class SourceInfoHandler(SourceHandler):
	def do_get(self):
		return 200, json.dumps({'name': self.source.source, 'url': self.source.url, 'revision': self.source.revision})

sources_base = '/sources/'
source_base = sources_base + '(' + sources.sources_allowed + ')'

routes = {sources_base: SourcesHandler, source_base: SourceInfoHandler}
