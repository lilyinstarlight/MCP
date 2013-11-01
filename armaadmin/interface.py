import os

from armaadmin import manager, sessions
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

	try:
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
			try:
				return server.getLog()
			except FileNotFoundError:
				return 'Log not found'
		elif request.request == '/get/scriptlog':
			try:
				return server.getScriptLog()
			except FileNotFoundError:
				return 'Script log not found'
		elif request.request == '/get/settings':
			try:
				return server.getSettings()
			except FileNotFoundError:
				return 'Settings file not found'
		elif request.request == '/get/script':
			try:
				return server.getScript()
			except FileNotFoundError:
				return 'Script file not found'
		elif request.request == '/update/settings':
			try:
				server.updateSettings(request.args.get('settings'))
			except FileNotFoundError:
				return 'Settings file not found'
		elif request.request == '/update/script':
			try:
				server.udpateScript(request.args.get('script'))
			except FileNotFoundError:
				return 'Script file not found'
	except NoServerError:
		return 'Server does not exist'
	except ServerRunningError:
		return 'Server is already running'
	except ServerStoppedError:
		return 'Server is not running'
	except:
		return 'Unknown error'

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

routes = { '/': root.handle, '/admin': admin.handle, '/api': api.handle, '/start': action, '/stop': action, '/reload': action, '/restart': action, '/status': action, '/sendcommand': action, '/get/log': action, '/get/scriptlog': action, '/get/settings': action, '/get/script': action, '/update/settings': action, '/update/script': action, '/admin/create/user': admin.action, '/admin/destroy/user': admin.action, '/admin/create/server': admin.action, '/admin/destroy/server': admin.action, '/admin/add/source': admin.action, '/admin/remove/source': admin.action, '/admin/update/source': admin.action, '/admin/get/users': admin.action, '/admin/get/servers': admin.action, '/admin/get/sources': admin.action, '/admin/get/config': admin.action, '/admin/update/config': admin.action, '404': file }
