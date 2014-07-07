import file
import pages
import api

from .. import config, log

httpd = None
routes = {}

file.init(os.path.dirname(__file__) + '/res', '/res')

routes.update(file.routes)
routes.update(pages.routes)
routes.update(api.routes)

httpd = web.HTTPServer(address, routes, log=log.httplog)
httpd.start()
