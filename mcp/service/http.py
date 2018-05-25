import fooster.web

import mcp.config
import mcp.api
import mcp.page


httpd = None
routes = {}

routes.update(mcp.api.routes)
routes.update(mcp.page.routes)


def start():
    global httpd

    httpd = fooster.web.HTTPServer((mcp.config.addr, mcp.config.port), routes, keyfile=mcp.config.tlskey, certfile=mcp.config.tlscert)
    httpd.start()


def stop():
    global httpd

    httpd.close()
    httpd = None


def join():
    global httpd

    httpd.join()
