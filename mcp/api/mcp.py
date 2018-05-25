import os
import signal

import mcp.common.pid
import mcp.common.http


class Restart(mcp.common.http.AuthHandler):
    def do_post(self):
        os.kill(mcp.common.pid.pid, signal.SIGUSR1)

        return 204, None


routes = {'/api/restart': Restart}
