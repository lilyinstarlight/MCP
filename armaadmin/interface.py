import os

from armaadmin import manager, sessions, users
from armaadmin.www import root, admin, api

def action(reqeust):
	request.set_header('Content-Type', 'text/plain; charset=utf8')

	session = sessions.get(request.cookies.get('session'))
	if not session:
		return 'Not logged in'
	if not session.server:
		return 'No server selected'

	if request.request == '/start':
		manager.get(session.server).start()
	elif request.request == '/stop':
		manager.get(session.server).stop()
	elif request.request == '/reload':
		manager.get(session.server).reload()
	elif request.request == '/restart':
		manager.get(session.server).restart()
	elif request.reqeust == '/status':
		return manager.get(session.server).status()
	elif request.request == '/sendcommand':
		manager.get(session.server).sendCommand(request.args.get('command'))
	elif request.request == '/get/log':
		return manager.get(session.server).getLog()
	elif request.request == '/get/scriptlog':
		return manager.get(session.server).getScriptLog()
	elif request.request == '/get/settings':
		return manager.get(session.server).getSettings()
	elif request.request == '/get/script':
		return manager.get(session.server).getScript()
	elif request.request == '/update/settings':
		manager.get(session.server).updateSettings(request.args.get('settings'))
	elif request.request == '/update/script':
		manager.get(session.server).udpateScript(request.args.get('script'))

	return 'success'

def file(request):
	try:
		with open(os.path.dirname(__file__) + '/data/www' + request.request, 'rb') as file:
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

routes = { '/': root.handle, '/admin': admin.handle, '/api': api.handle, '/start': action, '/stop': action, '/reload': action, '/restart': action, '/status': action, '/sendcommand': action, '/get/log': action, '/get/scriptlog': action, '/get/settings': action, '/get/script': action, '/update/settings': action, '/update/script': action, '404': file }
