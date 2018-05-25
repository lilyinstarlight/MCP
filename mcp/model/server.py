import os
import re

import fooster.db

import mcp.config
import mcp.error

import mcp.control.server

servers_allowed = '[0-9a-zA-Z-_+]+'

def items():
    return iter(server_db)

def get(server_name):
    return server_db.get(server_name)

def create(server_name, source_name, revision=None, port=None, autostart=True, users=[]):
    if not re.match('^' + servers_allowed + '$', server_name):
        raise mcp.error.InvalidServerError()

    if server_db.get(server_name):
        raise mcp.error.ServerExistsError()

    if not revision:
        revision = sources.get(source_name).revision

    if not port:
        port = port_get_next()

    if not port_check(port):
        raise mcp.error.InvalidPortError()

    if not port_is_available(port):
        raise mcp.error.PortExistsError()

    mcp.control.server.build(server_name, source_name, revision)

    mcp.control.server.set_port(server_name, port)

    return server_db.add(server_name, source_name, revision, port, autostart, users)

def modify(server_name, port=None, autostart=None, users=None):
    server_obj = server_db.get(server_name)

    if port != None:
        mcp.control.server.set_port(server_name, port)
        server_obj.port = port

    if autostart != None:
        server_obj.autostart = autostart

    if users:
        import mcp.users

        for username in users:
            user = mcp.users.get(username)
            if server_name not in user.servers:
                user.servers.append(server_name)

        server_obj.users = users

def upgrade(server_name, source_name=None, revision=None):
    server_obj = server_db.get(server_name)

    if not server_obj:
        raise mcp.error.NoServerError()

    if not source_name:
        source_name = server_obj.source

    if not revision:
        revision = sources.get(source_name).revision

    mcp.control.server.build(server_name, source_name, revision)

    server_obj.revision = revision

def destroy(server_name):
    if not server_db.get(server_name):
        raise mcp.error.NoServerError()

    mcp.control.server.destroy(server_name)

    server_db.remove(server_name)

def port_check(port):
    return port and port > 0 and port < 65536

def port_is_available(port):
    for server in server_db:
        if server.port == port:
            return False

    return True

def port_get_next():
    for port in range(*mcp.config.portrange):
        if port_is_available(port):
            return port

    return None

server_db = fooster.db.Database(mcp.config.database + '/servers.db', ['server', 'source', 'revision', 'port', 'autostart', 'users'])
