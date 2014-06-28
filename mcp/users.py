import hashlib
import os
import re

import errors

users = {}

users_allowed = re.compile('[0-9a-zA-Z-_+]+$')

class User:
	def __init__(self, name, password, servers, admin=False):
		self.name = name
		self.password = password
		self.servers = servers
		self.admin = admin

def parse():
	global users

	temp = {}

	with open(os.path.dirname(__file__) + '/users.db', 'r') as file:
		for line in file:
			data = line.rstrip().split('|')

			if data[2] == '':
				servers = []
			else:
				servers = data[2].split(',')

			if len(data) > 3:
				admin = data[3] == 'admin'
			else:
				admin = False

			if data[0] in users:
				user = users[data[0]]
				user.password = data[1]
				user.servers = servers
				user.admin = admin
				temp[data[0]] = user
			else:
				temp[data[0]] = User(data[0], data[1], servers, admin)

	users = temp

def check(user, password):
	return user in users and users[user].password == hashlib.sha256(password.encode()).hexdigest()

def get(user):
	return users.get(user)

def add(user, password, servers, admin=False):
	if user in users:
		raise errors.UserExistsError

	if not users_allowed.match(user):
		raise errors.InvalidUserError

	with open(os.path.dirname(__file__) + '/users.db', 'a') as file:
		if admin:
			file.write(user + '|' + hashlib.sha256(password.encode()).hexdigest() + '|' + ','.join(servers) + '|admin\n')
		else:
			file.write(user + '|' + hashlib.sha256(password.encode()).hexdigest() + '|' + ','.join(servers) + '\n')

	parse()

def modify(user, password=None, servers=None, admin=None):
	if not user in users:
		raise errors.NoUserError

	with open(os.path.dirname(__file__) + '/users.db', 'r') as file:
		lines = file.readlines()

	with open(os.path.dirname(__file__) + '/users.db', 'w') as file:
		for line in lines:
			if line.startswith(user + '|'):
				if password:
					new_pass = hashlib.sha256(password.encode()).hexdigest()
				else:
					new_pass = users[user].password

				if servers:
					new_servers = servers
				else:
					new_servers = users[user].servers

				if admin:
					file.write(user + '|' + new_pass + '|' + ','.join(new_servers) + '|admin\n')
				else:
					file.write(user + '|' + new_pass + '|' + ','.join(new_servers) + '\n')
			else:
				file.write(line)

	parse()

def remove(user):
	if not user in users:
		raise errors.NoUserError

	with open(os.path.dirname(__file__) + '/users.db', 'r') as file:
		lines = file.readlines()

	with open(os.path.dirname(__file__) + '/users.db', 'w') as file:
		for line in lines:
			if not line.startswith(user + '|'):
				file.write(line)

	parse()

parse()
