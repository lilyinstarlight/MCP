import json
import os

from armaadmin import errors, log, manager, sessions, sources, users

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
		if request.request == '/admin/get/users':
			user_list = {}
			for user in users.users:
				user_list[user] = { 'servers': users.users[user].servers, 'admin': users.users[user].admin }
			return json.dumps(user_list)
		elif request.request == '/admin/create/user':
			users.add(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin') == 'true')
		elif request.request == '/admin/modify/user':
			if request.args.get('password') == '':
				request.args['password'] = None
			users.modify(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin') == 'true')
		elif request.request == '/admin/destroy/user':
			users.remove(request.args.get('user'))
		elif request.request == '/admin/get/servers':
			server_list = {}
			for server in manager.servers:
				server_list[server] = { 'source': manager.servers[server].getSource(), 'revision': manager.servers[server].getRevision() }
			return json.dumps(server_list)
		elif request.request == '/admin/create/server':
			try:
				manager.create(request.args.get('server'), request.args.get('source'))
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/destroy/server':
			try:
				manager.destroy(request.args.get('server'))
			except errors.ConfigError:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/upgrade/server':
			try:
				manager.get(request.args.get('server')).upgrade()
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/upgrade/servers':
			try:
				for server in manager.servers:
					manager.servers[server].upgrade()
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif request.request == '/admin/get/sources':
			source_list = {}
			for source in sources.sources:
				source_list[source] = { 'revision': sources.sources[source].getRevision() }
			return json.dumps(source_list)
		elif request.request == '/admin/add/source':
			try:
				sources.add(request.args.get('source'), request.args.get('bzr'))
			except errors.BzrError as e:
				request.set_status(500)
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/remove/source':
			try:
				sources.remove(request.args.get('source'))
			except errors.ConfigError:
				request.set_status(500)
				return 'Error configuring source: ' + e.msg
		elif request.request == '/admin/update/source':
			try:
				sources.sources[request.args.get('source')].update()
			except errors.BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/update/sources':
			try:
				for source in sources.sources:
					sources.sources[source].update()
			except errors.BzrError as e:
				request.set_status(500)
				return 'Bzr command error: ' + e.msg
		elif request.request == '/admin/get/config':
			try:
				return sources.getConfig()
			except FileNotFoundError:
				return ''
		elif request.request == '/admin/update/config':
			sources.updateConfig(request.args.get('config'))
	except errors.NoServerCreationError:
		request.set_status(501)
		return 'Server creation is disabled'
	except errors.NoServerError:
		request.set_status(404)
		return 'Server not found'
	except errors.InvalidServerError:
		request.set_status(400)
		return 'Invalid server name'
	except errors.ServerExistsError:
		request.set_status(409)
		return 'Server already exists'
	except errors.NoSourceError:
		request.set_status(404)
		return 'Source not found'
	except errors.InvalidSourceError:
		request.set_status(400)
		return 'Invalid source name'
	except errors.SourceExistsError:
		request.set_status(409)
		return 'Source already exists'
	except errors.NoUserError:
		request.set_status(404)
		return 'User not found'
	except errors.InvalidUserError:
		request.set_status(400)
		return 'Invalid username'
	except errors.UserExistsError:
		request.set_status(409)
		return 'User already exists'
	except:
		log.exception('accessing "' + request.request + '"')
		request.set_status(500)
		return 'Unknown error'

	return ''

routes = { '/admin': handle, '/admin/get/users': action, '/admin/create/user': action, '/admin/modify/user': action, '/admin/destroy/user': action, '/admin/get/servers': action, '/admin/create/server': action, '/admin/destroy/server': action, '/admin/upgrade/server': action, '/admin/upgrade/servers': action, '/admin/get/sources': action, '/admin/add/source': action, '/admin/remove/source': action, '/admin/update/source': action, '/admin/update/sources': action, '/admin/get/config': action, '/admin/update/config': action }
