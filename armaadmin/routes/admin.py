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
		request.set_status(401)
		return 'Not logged in'
	if not session.user.admin:
		request.set_status(403)
		return 'Not an administrator'

	try:
		action = request.match.group(1)

		if action == 'get/users':
			user_list = {}
			for user in users.users:
				user_list[user] = { 'servers': users.users[user].servers, 'admin': users.users[user].admin }
			return json.dumps(user_list)
		elif action == 'create/user':
			users.add(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin') == 'true')
		elif action == 'modify/user':
			if request.args.get('password') == '':
				request.args['password'] = None
			users.modify(request.args.get('user'), request.args.get('password'), request.args.get('servers').split(','), request.args.get('admin') == 'true')
		elif action == 'destroy/user':
			users.remove(request.args.get('user'))
		elif action == 'get/servers':
			server_list = {}
			for server in manager.servers:
				server_list[server] = { 'source': manager.servers[server].getSource(), 'revision': manager.servers[server].getRevision() }
			return json.dumps(server_list)
		elif action == 'create/server':
			try:
				manager.create(request.args.get('server'), request.args.get('source'))
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif action == 'destroy/server':
			try:
				manager.destroy(request.args.get('server'))
			except errors.ConfigError:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif action == 'upgrade/server':
			try:
				manager.get(request.args.get('server')).upgrade()
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif action == 'upgrade/servers':
			try:
				for server in manager.servers:
					manager.servers[server].upgrade()
			except errors.BuildError as e:
				request.set_status(500)
				return 'Error building server: ' + e.msg
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring server: ' + e.msg
		elif action == 'get/sources':
			source_list = {}
			for source in sources.sources:
				source_list[source] = { 'revision': sources.sources[source].getRevision() }
			return json.dumps(source_list)
		elif action == 'add/source':
			try:
				sources.add(request.args.get('source'), request.args.get('bzr'))
			except errors.BzrError as e:
				request.set_status(500)
				return 'Bzr command error: ' + e.msg
		elif action == 'remove/source':
			try:
				sources.remove(request.args.get('source'))
			except errors.ConfigError as e:
				request.set_status(500)
				return 'Error configuring source: ' + e.msg
		elif action == 'update/source':
			try:
				sources.sources[request.args.get('source')].update()
			except errors.BzrError as e:
				return 'Bzr command error: ' + e.msg
		elif action == 'update/sources':
			try:
				for source in sources.sources:
					sources.sources[source].update()
			except errors.BzrError as e:
				request.set_status(500)
				return 'Bzr command error: ' + e.msg
		elif action == 'get/config':
			try:
				return sources.getConfig()
			except FileNotFoundError:
				return ''
		elif action == 'update/config':
			sources.updateConfig(request.args.get('config'))
		else:
			request.set_status(404)
			return '404 - Unknown action'
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

routes = { '/admin': handle, '/admin/([a-z/]+)': action }
