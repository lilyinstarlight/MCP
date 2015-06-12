from mcp import config, log
from mcp.interface import web, api, pages, res

httpd = None
routes = {}

routes.update(api.routes)
routes.update(pages.routes)
routes.update(res.routes)

def start():
	httpd = web.HTTPServer((config.host, config.port), routes, log=log.httplog)
	httpd.start()

def stop():
	httpd.close()
