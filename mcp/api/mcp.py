import os
import signal

import mcp.common.pid
import mcp.common.http


class Restart(mcp.common.http.AuthHandler):
    def do_post(self):
        # send SIGUSR1 to main process
        os.kill(mcp.common.daemon.pid, signal.SIGUSR1)

        return 204, None


routes = {'/api/restart': Restart}
