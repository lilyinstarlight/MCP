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

	try:
		if request.request == '/admin/create/user':
			users.add(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin') == 'true')
		elif request.request == '/admin/destroy/user':
			users.remove(request.args.get('user'))
		elif request.request == '/admin/create/server':
			try:
				manager.create(request.args.get('server'), request.args.get('source'))
			except BuildError as e:
				return 'Error building server: ' + e.msg
			except ConfigError as e:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/destroy/server':
			try:
				manager.destroy(request.args.get('server'))
			except ConfigError:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/add/source':
			try:
				server.addSource(request.args.get('source'), request.args.get('bzr'))
			except BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/remove/source':
			try:
				server.removeSource(request.args.get('source'))
			except ConfigError:
				return 'Error configuring source: ' + e.msg
		elif request.request == '/admin/update/source':
			try:
				server.updateSource(request.args.get('source'))
			except BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/get/users':
			return ','.join(users.users)
		elif request.request == '/admin/get/servers':
			return ','.join(manager.servers)
		elif request.request == '/admin/get/sources':
			return ','.join(server.getSources())
		elif request.request == '/admin/get/config':
			try:
				return server.getConfig()
			except FileNotFoundError:
				return 'Config file not found'
		elif request.request == '/admin/update/config':
			try:
				server.updateConfig(request.args.get('config'))
			except FileNotFoundError:
				return 'Config file not found'
	except NoServerCreationError:
		return 'Server creation is disabled'
	except ServerExistsError:
		return 'Server already exists'
	except NoSourceError:
		return 'Source not found'
	except SourceExistsError:
		return 'Source already exists'
	except:
		return 'Unknown error'

	return 'success'
