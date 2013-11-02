import os

from armaadmin import errors, manager, sessions, server, users

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
			except errors.BuildError as e:
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/destroy/server':
			try:
				manager.destroy(request.args.get('server'))
			except errors.ConfigError:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/upgrade/server':
			try:
				server.upgrade(request.args.get('server'))
			except errors.BuildError as e:
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/upgrade/servers':
			try:
				for server in manager.servers:
					server.upgrade(server)
			except errors.BuildError as e:
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/add/source':
			try:
				server.addSource(request.args.get('source'), request.args.get('bzr'))
			except errors.BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/remove/source':
			try:
				server.removeSource(request.args.get('source'))
			except errors.ConfigError:
				return 'Error configuring source: ' + e.msg
		elif request.request == '/admin/update/source':
			try:
				server.updateSource(request.args.get('source'))
			except errors.BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/update/sources':
			try:
				for source in server.getSources():
					server.updateSource(source)
			except errors.BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/get/users':
			return '\n'.join(users.users)
		elif request.request == '/admin/get/servers':
			return '\n,'.join(manager.servers)
		elif request.request == '/admin/get/sources':
			return '\n'.join(server.getSources())
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
	except errors.NoServerCreationError:
		return 'Server creation is disabled'
	except errors.ServerExistsError:
		return 'Server already exists'
	except errors.NoSourceError:
		return 'Source not found'
	except errors.SourceExistsError:
		return 'Source already exists'
	except errors.InvalidServerError:
		return 'Invalid server name'
	except errors.InvalidSourceError:
		return 'Invalid source name'
	except:
		return 'Unknown error'

	return 'success'

routes = { '/admin': handle, '/admin/create/user': action, '/admin/destroy/user': action, '/admin/create/server': action, '/admin/destroy/server': action, '/admin/upgrade/server': action, '/admin/upgrade/servers': action, '/admin/add/source': action, '/admin/remove/source': action, '/admin/update/source': action, '/admin/update/sources': action, '/admin/get/users': action, '/admin/get/servers': action, '/admin/get/sources': action, '/admin/get/config': action, '/admin/update/config': action }
