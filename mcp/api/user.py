import os
import signal

import fooster.web

import mcp.error

import mcp.common.http

import mcp.model.user


class Index(mcp.common.http.AuthHandler):
    def do_get(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        return 200, [dict(user) for user in mcp.model.user.items()]

    def do_post(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.user.add(self.request.body['username'], self.request.body['password'], admin=bool(self.request.body['admin'] if 'admin' in self.request.body else False))
        except (KeyError, TypeError):
            raise fooster.web.HTTPError(400)
        except mcp.error.InvalidUserError:
            raise fooster.web.HTTPError(403)
        except mcp.error.UserExistsError:
            raise fooster.web.HTTPError(409)

        self.response.headers['Location'] = '/api/user/' + self.request.body['username']

        return 201, dict(mcp.model.user.get(self.request.body['username']))

class User(mcp.common.http.AuthHandler):
    def do_get(self):
        if not self.auth.admin and self.groups[0] != self.auth.username:
            raise fooster.web.HTTPError(404)

        try:
            return 200, dict(mcp.model.user.get(self.groups[0]))
        except mcp.error.NoUserError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        if not self.auth.admin and self.groups[0] != self.auth.username:
            raise fooster.web.HTTPError(404)

        if ('admin' in self.request.body or 'active' in self.request.body or 'servers' in self.request.body) and not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.user.modify(self.groups[0], self.request.body['password'] if 'password' in self.request.body else None, self.request.body['key'] if 'key' in self.request.body else None, self.request.body['admin'] if 'admin' in self.request.body else None, self.request.body['active'] if 'active' in self.request.body else None, self.request.body['servers'] if 'servers' in self.request.body else None)
        except mcp.error.NoUserError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.user.get(self.groups[0]))

    def do_post(self):
        if not self.auth.admin and self.groups[0] != self.auth.username:
            raise fooster.web.HTTPError(404)

        try:
            return 200, {'token': mcp.model.user.create_token(self.groups[0])}
        except mcp.error.NoUserError:
            raise fooster.web.HTTPError(404)

    def do_delete(self):
        if not self.auth.admin and self.groups[0] != self.auth.username:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.user.destroy(self.groups[0])
        except mcp.error.NoUserError:
            raise fooster.web.HTTPError(404)

        return 204, None


routes = {'/api/user/': Index, '/api/user/(' + mcp.model.user.users_allowed + ')': User}
