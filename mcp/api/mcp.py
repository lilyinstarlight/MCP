import os
import signal

import fooster.web
import fooster.web.query

import mcp.config

import mcp.common.daemon
import mcp.common.http


class Features(mcp.common.http.AuthHandler):
    def do_get(self):
        # return enabled features
        return 200, {'creation': mcp.config.creation}

class Config(mcp.common.http.PlainAuthHandler):
    def do_get(self):
        # get config
        try:
            with open(mcp.config.config + '/server_info.cfg', 'r') as conf:
                return 200, conf.read()
        except FileNotFoundError:
            return 200, ''

    def do_put(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(401)

        # update config
        with open(mcp.config.config + '/server_info.cfg', 'w') as conf:
            conf.write(config)

        return 204, None

class Restart(mcp.common.http.AuthHandler):
    def do_post(self):
        if not self.auth.admin:
            raise fooster.web.HTTPError(401)

        # send SIGUSR1 to main process
        os.kill(mcp.common.daemon.pid, signal.SIGUSR1)

        return 204, None


routes = {'/api/features' + fooster.web.query.regex: Features, '/api/config' + fooster.web.query.regex: Config, '/api/restart' + fooster.web.query.regex: Restart}
