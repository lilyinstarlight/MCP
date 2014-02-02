import os

from armaadmin import name, version
from armaadmin.routes import root, admin, api

def file(request):
	try:
		with open(os.path.dirname(__file__) + '/www' + request.path, 'rb') as file:
			request.set_status(200)

			if request.path.endswith('.html'):
				request.set_header('Content-Type', 'text/html; charset=utf-8')
			elif request.path.endswith('.png'):
				request.set_header('Content-Type', 'image/png')
			elif request.path.endswith('.css'):
				request.set_header('Content-Type', 'text/css; charset=utf-8')
			elif request.path.endswith('.js'):
				request.set_header('Content-Type', 'application/javascript; charset=utf-8')
			else:
				request.set_header('Content-Type', 'text/plain; charset=utf-8')

			return file.read()
	except FileNotFoundError:
		request.set_header('Content-Type', 'text/plain; charset=utf-8')
		return '404 - Not Found'

def ver(request):
	return name + ' ' + version

routes = { '404': file, '/version': ver }
routes.update(root.routes)
routes.update(admin.routes)
routes.update(api.routes)
