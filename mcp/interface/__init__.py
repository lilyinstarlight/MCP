import file
import pages
import api

routes = {}

def init(address, log):
	file.init(os.path.dirname(__file__) + '/res', '/res')
	routes.update(file.routes)
	routes.update(pages.routes)
	routes.update(api.routes)
	web.init(address, routes, log=log)
