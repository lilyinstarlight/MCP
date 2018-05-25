import fooster.web
import fooster.web.json

import mcp.config
import mcp.api
import mcp.page


httpd = None
routes = {}
error_routes = {}

routes.update(mcp.api.routes)
routes.update(mcp.page.routes)

error_routes.update(fooster.web.json.new_error())


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
