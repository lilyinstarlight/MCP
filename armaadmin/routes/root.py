import json
import os

from armaadmin import errors, log, manager, sessions, users

def handle(request):
	error = ''

	session = sessions.get(request.cookies.get('session'))

	if request.args.get('user') and request.args.get('password'):
		if users.check(request.args.get('user'), request.args.get('password')):
			session = sessions.create()
			request.set_cookie({'session': session.id})
			session.user = users.get(request.args.get('user'))
		else:
			error += '<span class="failure">Error: Wrong username and/or password.</span><br /><br />'

	if 'logout' in request.args:
		sessions.destroy(request.cookies.get('session'))
		request.set_cookie({'session': '0'}, -1)
		session = None

	if session:
		request.set_cookie({'session': session.id})

		if session.user.admin:
			menu = '\n<a href="/admin" class="button">Admin</a>'
		else:
			menu = ''

		with open(os.path.dirname(__file__) + '/html/index.html', 'r') as file:
			return file.read() % { 'menu': menu }
	else:
		with open(os.path.dirname(__file__) + '/html/login.html', 'r') as file:
			return file.read() % { 'error': error, 'user': request.args.get('user', '') }

def action(request):
	request.set_header('Content-Type', 'text/plain; charset=utf8')

	session = sessions.get(request.cookies.get('session'))

	if not session:
		request.set_status(401)
		return 'Not logged in'

	servers = session.user.servers

	try:
		if request.request == '/servers':
			return json.dumps(servers)

		server_name = request.match.group(1)

		if not server_name in servers:
			request.set_status(403)
			return 'User not authorized for server'

		server = manager.get(server_name)

		if request.match.lastindex == 1:
			request.set_status(501)
			return 'TODO - General server info in JSON'

		action = request.match.group(2)

		if action == 'start':
			server.start()
		elif action == 'stop':
			server.stop()
		elif action == 'reload':
			server.reload()
		elif action == 'restart':
			server.restart()
		elif action == 'status':
			return server.status()
		elif action == 'sendcommand':
			server.sendCommand(request.args.get('command'))
		elif action == 'get/log':
			try:
				return server.getLog()
			except FileNotFoundError:
				return ''
		elif action == 'get/scriptlog':
			try:
				return server.getScriptLog()
			except FileNotFoundError:
				return ''
		elif action == 'get/settings':
			try:
				return server.getSettings()
			except FileNotFoundError:
				return ''
		elif action == 'get/script':
			try:
				return server.getScript()
			except FileNotFoundError:
				return ''
		elif action == 'update/settings':
			server.updateSettings(request.args.get('settings'))
		elif action == 'update/script':
			server.udpateScript(request.args.get('script'))
		else:
			request.set_status(404)
			return '404 - Unknown action'
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

routes = { '/': handle, '/servers': action, '/server/([0-9a-zA-Z-_+]+)': action, '/server/([0-9a-zA-Z-_+]+)/([a-z/]+)': action }
