import os

from armaadmin import manager, sessions, users
from armaadmin.routes import root, admin, api

def action(request):
	request.set_header('Content-Type', 'text/plain; charset=utf8')

	session = sessions.get(request.cookies.get('session'))
	if not session:
		return 'Not logged in'
	if not session.server:
		return 'No server selected'

	server = manager.get(session.server)

	if not server:
		return 'Server does not exist'

	if request.request == '/start':
		server.start()
	elif request.request == '/stop':
		server.stop()
	elif request.request == '/reload':
		server.reload()
	elif request.request == '/restart':
		server.restart()
	elif request.request == '/status':
		return server.status()
	elif request.request == '/sendcommand':
		server.sendCommand(request.args.get('command'))
	elif request.request == '/get/log':
		return server.getLog()
	elif request.request == '/get/scriptlog':
		return server.getScriptLog()
	elif request.request == '/get/settings':
		return server.getSettings()
	elif request.request == '/get/script':
		return server.getScript()
	elif request.request == '/update/settings':
		server.updateSettings(request.args.get('settings'))
	elif request.request == '/update/script':
		server.udpateScript(request.args.get('script'))
	elif request.request == '/admin/create/user':
		users.add(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin'))
	elif request.request == '/admin/destroy/user':
		users.remove(request.args.get('user'))
	elif request.request == '/admin/create/server':
		manager.create(request.args.get('server'))
	elif request.request == '/admin/destroy/server':
		manager.destroy(request.args.get('server'))

	return 'success'

def file(request):
	try:
		with open(os.path.dirname(__file__) + '/www' + request.request, 'rb') as file:
			request.set_status(200)

			if request.request.endswith('.html'):
				request.set_header('Content-Type', 'text/html; charset=utf-8')
			elif request.request.endswith('.png'):
				request.set_header('Content-Type', 'image/png')
			elif request.request.endswith('.css'):
				request.set_header('Content-Type', 'text/css; charset=utf-8')
			elif request.request.endswith('.js'):
				request.set_header('Content-Type', 'application/javascript; charset=utf-8')
			else:
				request.set_header('Content-Type', 'application/plain; charset=utf-8')

			return file.read()
	except IOError:
		request.set_header('Content-Type', 'text/plain; charset=utf-8')
		return '404 - Not Found'

routes = { '/': root.handle, '/admin': admin.handle, '/api': api.handle, '/start': action, '/stop': action, '/reload': action, '/restart': action, '/status': action, '/sendcommand': action, '/get/log': action, '/get/scriptlog': action, '/get/settings': action, '/get/script': action, '/update/settings': action, '/update/script': action, '/admin/create/user': action, '/admin/destroy/user': action, '/admin/create/server': action, '/admin/destroy/server': action, '404': file }
