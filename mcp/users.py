import hashlib
import os
import random
import re
import string

from . import db, errors

users_allowed = '^[0-9a-zA-Z-_+]+$'

key_length = 24
key_chars = string.ascii_letters + string.digits
key_rnd = random.SystemRandom()

def hash(password):
	return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
	user = user_db.get(username)

	if user and user.hash == hash(password):
		return user
	else:
		return None

def check_key(key):
	if key == '':
		return None

	for user in user_db:
		if user.key == key:
			return user

	return None

def gen_key(user):
	user.hash = ''.join(key_rnd.choice(key_chars) for _ in range(key_length))

def get(username):
	return user_db.get(username)

def add(username, password, key='', admin=False, active=True, servers=[]):
	if not re.match(users_allowed, username):
		raise errors.InvalidUserError()

	if user_db.get(username):
		raise errors.UserExistsError()

	return user_db.add(username, hash(password), key, admin, active, servers)

def modify(username, password=None, key=None, admin=None, active=None, servers=None):
	user = user_db.get(username)

	if not user:
		raise errors.NoUserError()

	if password:
		user.hash = hash(password)
	if key:
		user.key = key
	if admin:
		user.admin = admin
	if active:
		user.active = active
	if servers:
		user.servers = servers

def remove(username):
	if not user_db.get(username):
		raise errors.NoUserError()

	user_db.remove(username)

user_db = db.Database(os.path.dirname(__file__) + '/db/users.db', [ 'username', 'hash', 'key', 'admin', 'active', 'servers' ])
