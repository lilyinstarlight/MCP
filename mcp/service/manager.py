import logging
import multiprocessing
import os
import subprocess
import sys
import time
import traceback

import mcp.error

import mcp.common.env
import mcp.common.daemon

import mcp.model.server

log = logging.getLogger('mcp')

class Script(object):
    def __init__(self, server):
        self.server = server
        self.exe = self.server.prefix + '/scripts/script.py'

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
        return bool(self.proc and self.proc.poll())

    def is_quit(self):
        return bool(self.proc and self.proc.poll() == 0)

class Server(object):
    def __init__(self, metadata):
        self.name = metadata.server
        self.prefix = mcp.config.prefix + '/' + self.name
        self.exe = self.prefix + '/bin/armagetronad-dedicated'

        self.proc = None

        self.script = Script(self)

        if metadata.autostart:
            self.start()
        else:
            metadata.running = False
            metadata.script_running = False

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise mcp.error.ServerNonexistentError()

        self.proc = subprocess.Popen([self.exe, '--vardir', self.prefix + '/var', '--userdatadir', self.prefix + '/user', '--configdir', self.prefix + '/config', '--datadir', self.prefix + '/data'], stdin=subprocess.PIPE, stdout=open(self.prefix + '/server.log', 'a'), stderr=open(self.prefix + '/error.log', 'w'), env=mcp.common.env.get_server(), cwd=self.prefix)

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
        return bool(self.proc and self.proc.poll())

    def is_quit(self):
        return bool(self.proc and self.proc.poll() == 0)

    def send_command(self, command):
        if not self.is_running():
            raise mcp.error.ServerStoppedError()

        self.proc.stdin.write(command + '\n')

running = multiprocessing.Value('b', False)
process = None

def run(poll_interval=0.5):
    server_processes = {}

    for entry in mcp.model.server.items():
        server_processes[entry.server] = Server(entry)

        entry.running = False
        entry.script_running = False
        entry.command = ''

    try:
        while running.value:
            try:
                for entry in mcp.model.server.items():
                    # create process if necessary
                    if entry.server not in server_processes:
                        server_processes[entry.server] = Server(entry)

                        entry.running = False
                        entry.script_running = False
                        entry.command = ''

                    # get process
                    process = server_processes[entry.server]

                    # check if each server is supposed to be running and poll for problems
                    if entry.running:
                        for command in entry.command.split('\n'):
                            process.send_command(command)

                        if not process.proc:
                            process.start()
                        elif process.is_quit():
                            process.script.stop()
                            entry.script_running = False
                            process.stop()
                            entry.running = False
                            log.warning(process.name + ' stopped by itself.')
                        elif process.is_dead():
                            with open(process.prefix + '/server.log', 'a') as server_log:
                                server_log.write('WARNING: The server did not gracefully quit: now restarting.\n')
                            with open(process.prefix + '/error.log', 'a') as error_log:
                                error_log.write('WARNING: The server did not gracefully quit: now restarting.\n')
                            log.warning(process.name + ' did not gracefully quit.')
                            process.stop()
                            process.start()
                            log.warning(process.name + ' restarted.')

                        if entry.script_running:
                            if not process.script.proc:
                                process.script.start()
                            elif process.script.is_quit():
                                process.script.stop()
                                entry.script_running = False
                                log.warning(process.name + ' script stopped by itself.')
                            elif process.script.is_dead():
                                process.script.stop()
                                entry.script_running = False
                                log.warning(process.name + ' script did not gracefully quit.')
                    else:
                        entry.script_running = False

                        if process.script.is_running():
                            process.script.stop()
                        if process.is_running():
                            process.stop()

                for name in server_processes.keys():
                    if not mcp.model.server.get(name):
                        del server_processes[name]

                time.sleep(poll_interval)
            except:
                traceback.print_exc()
    finally:
        for process in server_processes.values():
            process.stop()

def start():
    global running, process

    if process:
        return

    running.value = True
    process = multiprocessing.Process(target=run, name='mcp-manager')
    process.start()

def stop():
    global running, process

    if not process:
        return

    running.value = False
    process.join()
    process = None

def is_running():
    return bool(process and process.is_alive())
