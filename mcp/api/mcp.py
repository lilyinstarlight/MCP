import os
import signal

import mcp.common.http


class Restart(mcp.common.http.AuthHandler):
    def do_post(self):
        os.kill(os.getpid(), signal.SIGUSR1)

        return 204, None


routes = {'/restart': Restart}
