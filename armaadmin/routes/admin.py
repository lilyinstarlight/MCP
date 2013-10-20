import os

from armaadmin import manager, sessions, server, users

def handle(request):
	session = sessions.get(request.cookies.get('session'))
	if not session or not session.user.admin:
		request.set_status(307)
		request.set_header('Location', '/')
		return ''

	with open(os.path.dirname(__file__) + '/html/admin.html', 'r') as file:
		return file.read()

def action(request):
	request.set_header('Content-Type', 'text/plain; charset=utf8')

	session = sessions.get(request.cookies.get('session'))

	if not session:
		return 'Not logged in'
	if not session.user.admin:
		return 'Not an administrator'

	if request.request == '/admin/create/user':
		users.add(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin'))
	elif request.request == '/admin/destroy/user':
		users.remove(request.args.get('user'))
	elif request.request == '/admin/create/server':
		manager.create(request.args.get('server'))
	elif request.request == '/admin/destroy/server':
		manager.destroy(request.args.get('server'))
	elif request.request == '/admin/get/users':
		return ','.join(users.users)
	elif request.request == '/admin/get/servers':
		return ','.join(manager.servers)
	elif request.request == '/admin/get/config':
		return server.getConfig()

	return 'success'
