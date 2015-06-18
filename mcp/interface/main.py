from mcp import config, log
from mcp.interface import web, api, pages

httpd = None
routes = {}

routes.update(api.routes)
routes.update(pages.routes)

def start():
	global httpd

	httpd = web.HTTPServer((config.host, config.port), routes, keyfile=config.tlskey, certfile=config.tlscert, log=log.httplog)
	httpd.start()

def stop():
	global httpd

	httpd.close()
	httpd = None
