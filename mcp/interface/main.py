from mcp import config, log
from mcp.interface import web, api, pages, res

httpd = None
routes = {}

routes.update(api.routes)
routes.update(pages.routes)
routes.update(res.routes)

def start():
	global httpd

	httpd = web.HTTPServer((config.host, config.port), routes, log=log.httplog)
	httpd.start()

def stop():
	global httpd

	httpd.close()
	httpd = None
