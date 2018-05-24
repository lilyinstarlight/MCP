from mcp import config, api, page

from fooster import web


httpd = None
routes = {}

routes.update(api.routes)
routes.update(page.routes)


def start():
    global httpd

    httpd = web.HTTPServer((config.addr, config.port), routes, keyfile=config.tlskey, certfile=config.tlscert)
    httpd.start()


def stop():
    global httpd

    httpd.close()
    httpd = None
