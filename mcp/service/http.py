from mcp import config, api, page

from mcp.common import log


httpd = None
routes = {}

routes.update(api.routes)
routes.update(page.routes)


def start():
    global httpd

    httpd = web.HTTPServer((config.host, config.port), routes, keyfile=config.tlskey, certfile=config.tlscert, log=log.httplog)
    httpd.start()


def stop():
    global httpd

    httpd.close()
    httpd = None
