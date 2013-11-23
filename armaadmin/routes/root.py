import os

from armaadmin import errors, manager, sessions, users

def handle(request):
	error = ''

	session = sessions.get(request.cookies.get('session'))

	if request.args.get('user') and request.args.get('password'):
		if users.check(request.args.get('user'), request.args.get('password')):
			session = sessions.create()
			request.set_cookie({'session': session.id})
			session.user = users.get(request.args.get('user'))
			if len(session.user.servers) > 0:
				session.server = session.user.servers[0]
			else:
				session.server = None
		else:
			error += '<span class="failure">Error: Wrong username and/or password.</span><br /><br />'

	if 'logout' in request.args:
		sessions.destroy(request.cookies.get('session'))
		request.set_cookie({'session': '0'}, -1)
		session = None

	if session:
		request.set_cookie({'session': session.id})

		server = request.args.get('server')
		if server and server in session.user.servers:
			session.server = server

		servers = ''
		for server in session.user.servers:
			if server == session.server:
				servers += '\n\t\t\t\t\t\t<option value="' + server + '" selected="selected">' + server + '</option>'
			else:
				servers += '\n\t\t\t\t\t\t<option value="' + server + '">' + server + '</option>'

		if session.user.admin:
			menu = '\n<a href="/admin" class="button">Admin</a>'
		else:
			menu = ''

		with open(os.path.dirname(__file__) + '/html/index.html', 'r') as file:
			return file.read() % { 'server': session.server, 'servers': servers, 'menu': menu }
	else:
		with open(os.path.dirname(__file__) + '/html/login.html', 'r') as file:
			return file.read() % { 'error': error, 'user': request.args.get('user', '') }

def action(request):
	request.set_header('Content-Type', 'text/plain; charset=utf8')

	session = sessions.get(request.cookies.get('session'))
	if not session:
		return 'Not logged in'
	if not session.server:
		return 'No server selected'

	try:
		server = manager.get(session.server)

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
				return ''
		elif request.request == '/get/scriptlog':
			try:
				return server.getScriptLog()
			except FileNotFoundError:
				return ''
		elif request.request == '/get/settings':
			try:
				return server.getSettings()
			except FileNotFoundError:
				return ''
		elif request.request == '/get/script':
			try:
				return server.getScript()
			except FileNotFoundError:
				return ''
		elif request.request == '/update/settings':
			server.updateSettings(request.args.get('settings'))
		elif request.request == '/update/script':
			server.udpateScript(request.args.get('script'))
	except errors.NoServerError:
		request.set_status(500)
		return 'Server does not exist'
	except errors.ServerRunningError:
		request.set_status(409)
		return 'Server is already running'
	except errors.ServerStoppedError:
		request.set_status(409)
		return 'Server is not running'
	except:
		log.exception('accessing "' + request.request + '"')
		request.set_status(500)
		return 'Unknown error'

	return ''

routes = { '/': handle, '/start': action, '/stop': action, '/reload': action, '/restart': action, '/status': action, '/sendcommand': action, '/get/log': action, '/get/scriptlog': action, '/get/settings': action, '/get/script': action, '/update/settings': action, '/update/script': action }
