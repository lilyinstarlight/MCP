import os
import signal

import fooster.web
import fooster.web.query

import mcp.error

import mcp.common.http

import mcp.model.script


class Index(mcp.common.http.AuthHandler):
    group = 0

    def do_get(self):
        # block if not an admin
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        return 200, [dict(library) for library in mcp.model.script.items()]

    def do_post(self):
        # block if not an admin
        if not self.auth.admin:
            raise fooster.web.HTTPError(403)

        try:
            # add requested source from URL
            mcp.model.script.add(self.request.body['name'], self.request.body['url'])
        except (KeyError, TypeError):
            # url parameters not found
            raise fooster.web.HTTPError(400)
        except mcp.error.BzrError:
            # bad bzr url
            raise fooster.web.HTTPError(400)
        except mcp.error.InvalidLibraryError:
            # invalid library name
            raise fooster.web.HTTPError(403)
        except mcp.error.LibraryExistsError:
            # library already exists
            raise fooster.web.HTTPError(409)

        # tell client where to find new script
        self.response.headers['Location'] = '/api/script/' + self.request.body['name']

        # return a copy of the new script
        return 201, dict(mcp.model.script.get(self.request.body['name']))

class Library(mcp.common.http.AuthHandler):
    group = 1

    def do_get(self):
        # ignore if not admin
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            return 200, dict(mcp.model.script.get(self.groups[0]))
        except mcp.error.NoLibraryError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        # ignore if not admin
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.script.update(self.groups[0])
        except mcp.error.NoLibraryError:
            raise fooster.web.HTTPError(404)

        return 200, dict(mcp.model.script.get(self.request.body['name']))

    def do_delete(self):
        # ignore if not admin
        if not self.auth.admin:
            raise fooster.web.HTTPError(404)

        try:
            mcp.model.script.destroy(self.groups[0])
        except mcp.error.NoLibraryError:
            raise fooster.web.HTTPError(404)

        return 204, None

class Documentation(mcp.common.http.PlainHandler):
    group = 1

    def do_get(self):
        self.response.headers['Content-Type'] = 'text/html'

        try:
            return 200, mcp.model.script.doc_get(self.groups[0])
        except mcp.error.NoLibraryError:
            raise fooster.web.HTTPError(404)

routes = {'/api/script/' + fooster.web.query.regex: Index, '/api/script/(' + mcp.model.script.libraries_allowed + ')' + fooster.web.query.regex: Library, '/api/script/(' + mcp.model.script.libraries_allowed + ')/doc' + fooster.web.query.regex: Documentation}
