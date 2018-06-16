import os
import signal

import fooster.web
import fooster.web.query

import mcp.error

import mcp.common.http

import mcp.model.server


class Index(mcp.common.http.AuthHandler):
    def do_get(self):
        return 200, [dict(server) for server in mcp.model.server.items() if self.auth.username in server.users or self.auth.admin]

    def do_post(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.server.create(self.request.body['server'], self.request.body['source'], self.request.body['revision'] if 'revision' in self.request.body else None, self.request.body['port'] if 'port' in self.request.body else None, self.request.body['autostart'] if 'autostart' in self.request.body else None)
        except (KeyError, TypeError):
            raise fooster.web.HTTPError(400)
        except mcp.error.NoSourceError:
            raise fooster.web.HTTPError(400)
        except mcp.error.InvalidServerError:
            raise fooster.web.HTTPError(403)
        except mcp.error.ServerExistsError:
            raise fooster.web.HTTPError(409)

        self.response.headers['Location'] = '/api/server/' + self.request.body['server']

        return 201, dict(mcp.model.server.get(self.request.body['server']))

class Server(mcp.common.http.AuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.server.get(self.groups[0]))

    def do_post(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.server.send(self.groups[0], self.request.body)
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

        return 204, None

    def do_put(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        if not self.auth.admin and ('port' in self.request.body or 'source' in self.request.body or 'revision' in self.request.body):
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.server.modify(self.groups[0], self.request.body['port'] if 'port' in self.request.body else None, self.request.body['autostart'] if 'autostart' in self.request.body else None, self.request.body['users'] if 'users' in self.request.body else None)

            if 'source' in self.request.body or 'revision' in self.request.body:
                mcp.model.server.upgrade(self.groups[0], self.request.body['source'] if 'source' in self.request.body else None, self.request.body['revision'] if 'revision' in self.request.body else None)

            mcp.model.server.stop(self.groups[0])
            if 'running' in self.request.body and self.request.body['running']:
                mcp.model.server.start(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.server.get(self.groups[0]))

    def do_delete(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.server.stop(self.groups[0])
            mcp.model.server.destroy(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

        return 204, None

class Settings(mcp.common.http.PlainAuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            return 200, mcp.model.server.settings_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            mcp.model.server.settings_set(self.groups[0], self.request.body)

            return 200, mcp.model.server.settings_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

    def do_delete(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.server.settings_remove(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

        return 204, None

class Log(mcp.common.http.PlainAuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            try:
                return 200, mcp.model.server.log_get(self.groups[0], int(self.request.query['last']) if 'last' in self.request.query else None)
            except mcp.error.LastLogLine:
                return 204, ''
            except mcp.error.NoLogLine:
                return 201, mcp.model.server.script_log_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

class Script(mcp.common.http.PlainAuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'application/x-python-code'

        try:
            return 200, mcp.model.server.script_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'application/x-python-code'

        try:
            mcp.model.server.script_stop(self.groups[0])
            if self.request.body:
                mcp.model.server.script_set(self.groups[0], self.request.body)
            mcp.model.server.script_start(self.groups[0])

            return 200, mcp.model.server.script_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

    def do_delete(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.server.script_stop(self.groups[0])

            mcp.model.server.script_remove(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)

        return 204, None

class ScriptLog(mcp.common.http.PlainAuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except AttributeError:
            raise fooster.web.HTTPError(404)

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            try:
                return 200, mcp.model.server.script_log_get(self.groups[0], int(self.request.query['last']) if 'last' in self.request.query else None)
            except mcp.error.LastLogLine:
                return 204, ''
            except mcp.error.NoLogLine:
                return 201, mcp.model.server.script_log_get(self.groups[0])
        except mcp.error.NoServerError:
            raise fooster.web.HTTPError(404)


routes = {'/api/server/' + fooster.web.query.regex: Index, '/api/server/(' + mcp.model.server.servers_allowed + ')' + fooster.web.query.regex: Server, '/api/server/(' + mcp.model.server.servers_allowed + ')/settings' + fooster.web.query.regex: Settings, '/api/server/(' + mcp.model.server.servers_allowed + ')/log' + fooster.web.query.regex: Log, '/api/server/(' + mcp.model.server.servers_allowed + ')/script' + fooster.web.query.regex: Script, '/api/server/(' + mcp.model.server.servers_allowed + ')/script/log' + fooster.web.query.regex: ScriptLog}
