import hashlib

users = {}

def parse():
	del users[:]

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'r') as file:
		for line in file:
			data = line.rstrip().split('|')
			if len(data) > 3:
				users[data[0]] = User(data[0], data[1], data[2].split(','), data[3] == 'admin')
			else:
				users[data[0]] = User(data[0], data[1], data[2].split(','))

def check(user, password):
	return user in users and users[user].password == hashlib.sha256(password.encode()).hexdigest()

def get(user):
	return users.get(user)

def add(user, password, servers, admin=False):
	if user in users:
		return

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'a') as file:
		if admin:
			file.write(user + '|' + hashlib.sha256(password.encode()).hexdigest() + '|' + ','.join(servers) + '|admin\n')
		else:
			file.write(user + '|' + hashlib.sha256(password.encode()).hexdigest() + '|' + ','.join(servers) + '\n')

	parse()

def change(user, password=None, servers=None, admin=None):
	if not user in users:
		return

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'r') as file:
		lines = file.readlines()

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'w') as file:
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
	if user in users:
		return

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'r') as file:
		lines = file.readlines()

	with open(os.path.join(os.path.dirname(__file__), 'users.db'), 'w') as file:
		for line in lines:
			if not line.startswith(user + '|'):
				file.write(line)

	parse()

class User:
	def __init__(self, name, password, servers, admin=False):
		self.name = name
		self.password = password
		self.servers = servers
		self.admin = admin

parse()
