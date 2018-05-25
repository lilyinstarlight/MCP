import os
import signal

import fooster.web

import mcp.common.http
import mcp.model.script


class Index(mcp.common.http.AuthHandler):
    def do_get(self):
        return 200, list(script.items())

    def do_post(self):
        try:
            script.add(self.request.body['name'], self.request.body['url'])
        except KeyError:
            raise fooster.web.HTTPError(400)

        self.response.headers['Location'] = '/script/' + self.request.body['name']

        return 201, script.get(self.request.body['name'])

class Library(mcp.common.http.AuthHandler):
    def do_get(self):
        try:
            return 200, mcp.model.script.get(self.groups[0])
        except errors.NoScriptError:
            raise fooster.web.HTTPError(404)

    def do_put(self):
        try:
            mcp.model.script.update(self.groups[0])
        except errors.NoScriptError:
            raise fooster.web.HTTPError(404)

        return 200, mcp.model.script.get(self.request.body['name'])

    def do_delete(self):
        try:
            mcp.model.script.update(self.groups[0])
        except errors.NoScriptError:
            raise fooster.web.HTTPError(404)

        return 200, mcp.model.script.get(self.request.body['name'])


routes = {'/script/': Index, '/script/(' + mcp.model.script.libraries_allowed + ')': Library}
