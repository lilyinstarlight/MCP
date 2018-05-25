import os
import signal

import fooster.web

import mcp.error

import mcp.common.http

import mcp.model.script


class Index(mcp.common.http.AuthHandler):
    def do_get(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        return 200, [dict(library) for library in mcp.model.script.items()]

    def do_post(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            mcp.model.script.add(self.request.body['name'], self.request.body['url'])
        except KeyError:
            raise fooster.web.HTTPError(400)
        except mcp.error.InvalidLibraryError:
            raise fooster.web.HTTPError(403)
        except mcp.error.LibraryExistsError:
            raise fooster.web.HTTPError(409)

        self.response.headers['Location'] = '/api/script/' + self.request.body['name']

        return 201, dict(mcp.model.script.get(self.request.body['name']))

class Library(mcp.common.http.AuthHandler):
    def do_get(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            return 200, dict(mcp.model.script.get(self.groups[0]))
        except errors.NoLibraryError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.script.update(self.groups[0])
        except errors.NoLibraryError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.script.get(self.request.body['name']))

    def do_delete(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.script.destroy(self.groups[0])
        except errors.NoLibraryError:
            raise fooster.web.HTTPError(404)

        return 204, None


routes = {'/api/script/': Index, '/api/script/(' + mcp.model.script.libraries_allowed + ')': Library}
