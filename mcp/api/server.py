import os
import signal

import fooster.web

import mcp.error

import mcp.common.http

import mcp.model.server


class Index(mcp.common.http.AuthHandler):
    def do_get(self):
        return 200, [dict(server) for server in mcp.model.server.items() if self.auth.username in server.users]

    def do_post(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.server.create(self.request.body['name'], self.request.body['source'], self.request.body['revision'] if 'revision' in self.request.body else None, self.request.body['port'] if 'port' in self.request.body else None, self.request.body['autostart'] if 'autostart' in request.body else None)
        except KeyError:
            raise fooster.web.HTTPError(400)
        except mcp.error.InvalidServerError:
            raise fooster.web.HTTPError(403)
        except mcp.error.ServerExistsError:
            raise fooster.web.HTTPError(409)

        self.response.headers['Location'] = '/api/server/' + self.request.body['name']

        return 201, dict(mcp.model.server.get(self.request.body['name']))

class Server(mcp.common.http.AuthHandler):
    def do_get(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except errors.NoServerError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.server.get(self.groups[0]))

    def do_put(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except errors.NoServerError:
            raise fooster.web.HTTPError(404)

        if not self.auth.admin and ('port' in self.request.body or 'source' in self.request.body or 'revision' in self.request.body):
            raise fooster.web.HTTPError(403)

        mcp.model.server.modify(self.groups[0], self.request.body['port'] if 'port' in self.request.body else None, self.request.body['autostart'] if 'autostart' in self.request.body else None, self.request.body['users'] if 'users' in self.request.body else None)

        if 'source' in self.request.body or 'revision' in self.request.body:
            mcp.model.server.upgrade(self.groups[0], self.request.body['source'] if 'source' in self.request.body else None, self.request.body['revision'] if 'revision' in self.request.body else None)

        mcp.services.manager.get(self.groups[0]).stop()
        mcp.services.manager.get(self.groups[0]).start()

        return 200, dict(mcp.model.server.get(self.request.body['name']))

    def do_delete(self):
        try:
            if not self.auth.admin and self.auth.username not in mcp.model.server.get(self.groups[0]).users:
                raise fooster.web.HTTPError(404)
        except errors.NoServerError:
            raise fooster.web.HTTPError(404)

        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        mcp.services.manager.get(self.groups[0]).stop()

        mcp.model.server.destroy(self.groups[0])

        return 204, None


routes = {'/api/server/': Index, '/api/server/(' + mcp.model.server.servers_allowed + ')': Server}
