import logging
import multiprocessing
import os
import subprocess
import sys
import time

import mcp.error

import mcp.common.env
import mcp.model.server

log = logging.getLogger('mcp')

class Script(object):
    def __init__(self, server):
        self.server = server
        self.exe = self.prefix + '/scripts/script.py'

        self.proc = None

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise mcp.error.ScriptNonExistentError()

        self.proc = subprocess.Popen([sys.executable, self.server.prefix + '/scripts/script.py'], stdin=open(self.server.prefix + '/var/ladderlog.txt', 'r'), stdout=self.server.proc.stdin, stderr=open(self.server.prefix + '/script-error.log', 'w'), env=mcp.common.env.get_script(), cwd=self.server.prefix + '/var')

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
        self.prefix = config.prefix + '/' + self.name
        self.exe = self.prefix + '/bin/armagetronad-dedicated'

        self.proc = None

        self.script = Script(self)

        if metadata.autostart:
            self.start()

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise mcp.error.ServerNonexistentError()

        self.proc = subprocess.Popen([self.bin, '--vardir', self.prefix + '/var', '--userdatadir', self.prefix + '/user', '--configdir', self.prefix + '/config', '--datadir', self.prefix + '/data'], stdin=subprocess.PIPE, stdout=open(self.prefix + '/server.log', 'a'), stderr=open(self.prefix + '/error.log', 'w'), env=mcp.common.env.get_server(), cwd=self.prefix)

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
        return self.proc and self.proc.poll() == None

    def is_dead(self):
        return self.proc and self.proc.poll()

    def is_quit(self):
        return self.proc and self.proc.poll() == 0

    def send_command(self, command):
        if not self.is_running():
            raise mcp.error.ServerStoppedError()

        self.proc.stdin.write(command + '\n')

server_list = {}

running = False
process = None

def get(server_name):
    return server_list.get(server_name)

def create(server_name, source_name, revision=None, port=0, autostart=True, users=[]):
    entry = mcp.model.server.create(server_name, source_name, revision, port, autostart, users)
    server_list[entry.server] = Server(entry)

def destroy(server_name):
    if server_list.get(server_name).is_running():
        raise mcp.error.ServerRunningError()

    mcp.model.server.destroy(server_name)
    del server_list[server_name]

def run(poll_interval=0.5):
    server_list.clear()
    for entry in mcp.model.server.items():
        server_list[entry.server] = Server(entry)

    try:
        while running:
            for server in server_list.values():
                # check if each server is supposed to be running and poll for problems
                if server.proc:
                    if server.is_quit():
                        server.stop()
                        log.warning(server.name + ' stopped by itself.')
                    elif server.is_dead():
                        server.proc.stdout.write('WARNING: The server did not gracefully quit: now restarting.\n')
                        log.warning(server.name + ' did not gracefully quit.')
                        server.stop()
                        server.start()
                        log.warning(server.name + ' restarted.')

                    if server.script.proc:
                        if server.script.is_quit():
                            server.script.stop()
                            log.warning(server.name + ' script stopped by itself.')
                        elif server.script.is_dead():
                            server.script.stop()
                            log.warning(server.name + ' script did not gracefully quit.')

            time.sleep(poll_interval)
    finally:
        for server in server_list:
            server.stop()

def start():
    global running, process

    if is_running():
        return

    running = True
    process = multiprocessing.Process(target=run)
    process.start()

def stop():
    global running, process

    if not is_running():
        return

    running = False
    process.join()
    process = None

def is_running():
    return bool(process and process.is_alive())
