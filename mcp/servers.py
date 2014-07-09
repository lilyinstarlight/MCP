import os
import re

import db, errors, server

servers_allowed = re.compile('^[0-9a-zA-Z-_+]+$')

def get(server_name):
	return server_db.get(server_name)

def create(server_name, source, revision=None, port=None, users=[]):
	if server_db.get(server_name):
		raise errors.ServerExistsError()

	if not servers_allowed.match(server_name):
		raise errors.InvalidServerError()

	server.build(server_name, source, revision)

	server_db.add(server, source, revision, port, users)

def modify(server_name, port=None, users=None):
	server_obj = server_db.get(server_name)

	if port:
		server.set_port(server_name, port)
		server_obj.port = port

	if users:
		server_obj.users = users

def upgrade(server_name, source=None, revision=None):
	server_obj = server_db.get(server_name)

	if not server_obj:
		raise errors.NoServerError()

	if not source:
		source = server_obj.source

	server.build(server_name, source, revision)

	server_obj.revision = revision

def remove(server_name)
	if not server_db.get(server_name):
		raise errors.NoServerError()

	server.destroy(server_name)

	server_db.remove(server_name)

server_db = db.Database(os.path.dirname(__file__) + '/db/servers.db', [ 'server', 'source', 'revision', 'port', 'users' ])
