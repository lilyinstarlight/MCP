import logging
import os
import subprocess
import sys
import threading
import time

from mcp.common import env, error
from mcp.model import server

log = logging.getLogger('mcp')

class Script(object):
    def __init__(self, serve):
        self.server = serve
        self.exe = self.prefix + '/scripts/script.py'

        self.proc = None

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise errors.ScriptNonExistentError()

        self.proc = subprocess.Popen([sys.executable, self.server.prefix + '/scripts/script.py'], stdin=open(self.server.prefix + '/var/ladderlog.txt', 'r'), stdout=self.server.proc.stdin, stderr=open(self.server.prefix + '/script-error.log', 'w'), env=env.get_script(), cwd=self.server.prefix + '/var')

    def stop(self):
        if self.is_running():
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

        self.proc = None

    def is_running(self):
        return bool(self.proc and self.proc.poll() == None)

    def is_dead(self):
        return self.proc and self.proc.poll()

    def is_quit(self):
        return self.proc and self.proc.poll() == 0

class Server(object):
    def __init__(self, metadata):
        self.name = metadata.server
        self.metadata = metadata
        self.prefix = config.prefix + '/' + self.name
        self.exe = self.prefix + '/bin/armagetronad-dedicated'

        self.proc = None

        self.script = Script(self)

        if self.metadata.autostart:
            self.start()

    def exists(self):
        return os.path.isfile(self.exe)

    def upgrade(self, source_name=None, revision=None):
        if self.is_running():
            raise errors.ServerRunningError()

        server.upgrade(self.name, source_name, revision)

    def modify_metadata(self, port=None, autostart=None, users=None):
        server.modify(self.name, port, autostart, users)

        self.metadata = server.get(self.name)

    def start(self):
        if not self.exists():
            raise errors.ServerNonexistentError()

        self.proc = subprocess.Popen([self.bin, '--vardir', self.prefix + '/var', '--userdatadir', self.prefix + '/user', '--configdir', self.prefix + '/config', '--datadir', self.prefix + '/data'], stdin=subprocess.PIPE, stdout=open(self.prefix + '/server.log', 'a'), stderr=open(self.prefix + '/error.log', 'w'), env=env.get_server(), cwd=self.prefix)

        if self.script.exists():
            self.script.start()

    def stop(self):
        self.script.stop()

        if self.is_running():
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

        self.proc = None

    def reload(self):
        self.send_command('INCLUDE settings.cfg')
        self.send_command('INCLUDE server_info.cfg')
        self.send_command('INCLUDE settings_custom.cfg')

    def is_running(self):
        return bool(self.proc and self.proc.poll() == None)

    def is_dead(self):
        return self.proc and self.proc.poll()

    def is_quit(self):
        return self.proc and self.proc.poll() == 0

    def send_command(self, command):
        if not self.is_running():
            raise errors.ServerStoppedError()

        self.proc.stdin.write(command + '\n')

server_list = {}

running = False
thread = None

def get(server_name):
    return server_list.get(server_name)

def create(server_name, source_name, revision=None, port=0, autostart=True, users=[]):
    entry = server.create(server_name, source_name, revision, port, autostart, users)
    server_list[entry.server] = Server(entry)

def destroy(server_name):
    if server_list.get(server_name).is_running():
        raise errors.ServerRunningError()

    server.destroy(server_name)
    del server_list[server_name]

def run(poll_interval=0.5):
    server_list.clear()
    for entry in server.server_db:
        server_list[entry.server] = Server(entry)

    try:
        while running:
            for serve in server_list.values():
                # check if each server is supposed to be running and poll for problems
                if serve.proc:
                    if serve.is_quit():
                        serve.stop()
                        log.warning(server.name + ' stopped by itself.')
                    elif serve.is_dead():
                        serve.proc.stdout.write('WARNING: The server did not gracefully quit: now restarting.\n')
                        log.warning(server.name + ' did not gracefully quit.')
                        serve.stop()
                        serve.start()
                        log.warning(server.name + ' restarted.')

                    if serve.script.proc:
                        if serve.script.is_quit():
                            serve.script.stop()
                            log.warning(server.name + ' script stopped by itself.')
                        elif serve.script.is_dead():
                            serve.script.stop()
                            log.warning(server.name + ' script did not gracefully quit.')

            time.sleep(poll_interval)
    finally:
        for serve in server_list:
            serve.stop()

def start():
    global running, thread

    if is_running():
        return

    running = True
    thread = threading.Thread(target=run)
    thread.start()

def stop():
    global running, thread

    if not is_running():
        return

    running = False
    thread.join()
    thread = None

def is_running():
    return bool(thread and thread.is_alive())
