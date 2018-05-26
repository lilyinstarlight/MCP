import hashlib
import os
import random
import re
import string

import fooster.db

import mcp.config
import mcp.error

users_allowed = '[0-9a-zA-Z-_+]+'

key_length = 24
salt_length = 8

rand_chars = string.ascii_letters + string.digits
rand_rng = random.SystemRandom()

def hash(password, salt):
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

def check_user(username, password):
    user = user_db.get(username)

    if user and user.hash == hash(password, user.salt):
        return user

    raise mcp.error.NoUserError()

def check_key(key):
    if not key:
        return None

    for user in user_db:
        if user.key == key:
            return user

    raise mcp.error.NoUserError()

def gen_rand(length):
    return ''.join(rand_rng.choice(rand_chars) for _ in range(length))

def gen_key():
    return gen_rand(key_length)

def gen_salt():
    return gen_rand(salt_length)

def items():
    return iter(user_db)

def get(username):
    return user_db.get(username)

def add(username, password, salt=None, key=None, admin=False, active=True, servers=[]):
    if not re.match('^' + users_allowed + '$', username):
        raise mcp.error.InvalidUserError()

    if username in user_db:
        raise mcp.error.UserExistsError()

    if not salt:
        salt = gen_salt()

    user = user_db.Entry(username, hash(password, salt), salt, key, admin, active, servers)

    user_db[username] = user

    return user

def modify(username, password=None, key=None, admin=None, active=None, servers=None):
    try:
        user = user_db.get(username)
    except KeyError as error:
        raise mcp.error.NoUserError() from error

    if password:
        user.hash = hash(password, user.salt)

    if key:
        user.key = key

    if admin:
        user.admin = admin

    if active:
        user.active = active

    if servers:
        import mcp.model.server

        for server_name in servers:
            server = mcp.servers.get(server_name)
            if username not in server.users:
                server.users.append(username)

        user.servers = servers

def remove(username):
    # TODO: turn into an except thingy
    if not user_db.get(username):
        raise mcp.error.NoUserError()

    user_db.remove(username)

user_db = fooster.db.Database(mcp.config.database + '/db/users.db', ['username', 'hash', 'salt', 'key', 'admin', 'active', 'servers'])
