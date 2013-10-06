import os

from armaadmin import sessions, users

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

		with open(os.path.dirname(__file__) + '/html/index.html', 'r') as file:
			return file.read() % { 'server': session.server, 'servers': servers }
	else:
		with open(os.path.dirname(__file__) + '/html/login.html', 'r') as file:
			return file.read() % { 'error': error, 'user': request.args.get('user', '') }
