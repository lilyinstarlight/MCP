import os
import os.path
import re
import time

import fooster.db

import mcp.config
import mcp.error

import mcp.model.source

import mcp.control.server

servers_allowed = '[0-9a-zA-Z-_+][0-9a-zA-Z-_+.]*'

def items():
    return iter(server_db)

def get(server_name):
    return server_db.get(server_name)

def create(server_name, source_name, library_name=None, revision=None, port=None, autostart=True, users=[]):
    if not re.match('^' + servers_allowed + '$', server_name):
        raise mcp.error.InvalidServerError()

    if not re.match('^' + servers_allowed + '$', source_name):
        raise mcp.error.InvalidSourceError()

    if library_name and not re.match('^' + servers_allowed + '$', library_name):
        raise mcp.error.InvalidLibraryError()

    if server_name in server_db:
        raise mcp.error.ServerExistsError()

    if not mcp.model.source.get(source_name):
        raise mcp.error.NoSourceError()

    if library_name and not mcp.model.script.get(library_name):
        raise mcp.error.NoLibraryError()

    if not revision:
        revision = mcp.model.source.get(source_name).revision

    if not port:
        port = port_get_next()

    if not port_check(port):
        raise mcp.error.InvalidPortError()

    if not port_is_available(port):
        raise mcp.error.PortExistsError()

    mcp.control.server.build(server_name, source_name, library_name, revision)

    mcp.control.server.set_port(server_name, port)

    return server_db.add(server_name, source_name, library_name, revision, port, autostart, users, False, False, False, '', False)

def modify(server_name, library=None, port=None, autostart=None, users=None):
    try:
        server = server_db[server_name]
    except KeyError:
        raise mcp.error.NoServerError()

    if library:
        server.script = library
        server.reload = True

    if port is not None:
        mcp.control.server.set_port(server_name, port)
        server.port = port

    if autostart is not None:
        server.autostart = autostart

    if users:
        for username in server.users:
            server = mcp.servers.get(username)
            if server_name in user.servers and username not in users:
                user.servers.remove(server_name)

        for username in users:
            server = mcp.model.user.get(username)
            if server_name not in user.servers:
                user.servers.append(server_name)

        server.users = users

def upgrade(server_name, source_name=None, library_name=None, revision=None):
    try:
        server = server_db[server_name]
    except KeyError:
        raise mcp.error.NoServerError()

    if not source_name:
        source_name = server.source

    if not library_name:
        library_name = server.library

    if not revision:
        revision = mcp.model.source.get(source_name).revision

    mcp.control.server.build(server_name, source_name, library_name, revision)

    server.revision = revision

def destroy(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    if server_db[server_name].running:
        raise mcp.error.ServerRunningError()

    for username in server.users:
        user = mcp.model.user.get(username)
        if server_name in user.servers:
            user.servers.remove(server_name)

    mcp.control.server.destroy(server_name)

    del server_db[server_name]

def start(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    server_db[server_name].waiting = True
    server_db[server_name].running = True
    server_db[server_name].script_running = True

def stop(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    server_db[server_name].waiting = True
    server_db[server_name].script_running = False
    server_db[server_name].running = False

def wait(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    while server_db[server_name].waiting:
        time.sleep(mcp.config.poll_interval)

def log_get(server_name, last=None):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    try:
        with open(os.path.join(mcp.config.prefix, server_name, 'server.log'), 'rb') as log:
            if last:
                lines = len(log.readlines())
                log.seek(0)

                if lines + 1 == last:
                    raise mcp.error.LastLogLine()
                elif lines + 1 < last:
                    raise mcp.error.NoLogLine()

                for _ in range(last):
                    log.readline()

            contents = log.read()

            if contents and contents[-1] != b'\n':
                contents += b'\n'

            return contents
    except FileNotFoundError:
        return ''

def settings_get(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    try:
        with open(os.path.join(mcp.config.prefix, server_name, 'config', 'settings_custom.cfg'), 'rb') as settings_file:
            return settings_file.read()
    except FileNotFoundError:
        return ''

def settings_set(server_name, settings):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    with open(os.path.join(mcp.config.prefix, server_name, 'config', 'settings_custom.cfg'), 'wb') as settings_file:
        settings_file.write(settings)

def script_log_get(server_name, last=None):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    try:
        with open(os.path.join(mcp.config.prefix, server_name, 'script-error.log'), 'rb') as log:
            if last:
                lines = len(log.readlines())
                log.seek(0)

                if lines + 1 == last:
                    raise mcp.error.LastLogLine()
                elif lines + 1 < last:
                    raise mcp.error.NoLogLine()

                for _ in range(last):
                    log.readline()

            contents = log.read()

            if contents and contents[-1] != b'\n':
                contents += b'\n'

            return contents
    except FileNotFoundError:
        return ''

def script_start(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    server_db[server_name].waiting = True
    server_db[server_name].script_running = True

def script_stop(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    server_db[server_name].waiting = True
    server_db[server_name].script_running = False

def script_get(server_name):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    try:
        with open(os.path.join(mcp.config.prefix, server_name, 'script', 'script.py'), 'rb') as script_file:
            return script_file.read()
    except FileNotFoundError:
        return ''

def script_set(server_name, script):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    with open(os.path.join(mcp.config.prefix, server_name, 'script', 'script.py'), 'wb') as script_file:
        script_file.write(script)

def send(server_name, command):
    if server_name not in server_db:
        raise mcp.error.NoServerError()

    server_db[server_name].waiting = True
    server_db[server_name].command = '\n'.join(server_db[server_name].command.split('\n') + [command])

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

server_db = fooster.db.Database(os.path.join(mcp.config.database, 'servers.db'), ['server', 'source', 'library', 'revision', 'port', 'autostart', 'users', 'running', 'script_running', 'reload', 'command', 'waiting'])

import mcp.model.user
