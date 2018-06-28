import logging
import multiprocessing
import os
import os.path
import subprocess
import sys
import time
import traceback

import mcp.config
import mcp.error

import mcp.common.env
import mcp.common.daemon

import mcp.model.server

log = logging.getLogger('mcp')

class Script(object):
    def __init__(self, server):
        self.server = server
        self.exe = os.path.join(self.server.prefix, 'script', 'script.py')

        self.proc = None

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise mcp.error.ScriptNonexistentError()

        if mcp.config.container:
            self.proc = subprocess.Popen(['/usr/local/bin/mcp-container-helper', self.server.prefix, os.path.join('/', 'srv', 'script', 'bin', 'python'), os.path.join('/', 'srv', 'script', 'script.py')], stdin=open(os.path.join(self.server.prefix, 'var', 'ladderlog.txt'), 'r'), stdout=self.server.proc.stdin, stderr=open(os.path.join(self.server.prefix, 'script-error.log'), 'w'), env=mcp.common.env.get_script(), cwd=self.server.prefix)
        else:
            self.proc = subprocess.Popen([os.path.join(self.server.prefix, 'script', 'bin', 'python'), sys.executable, os.path.join(self.server.prefix, 'script', 'script.py')], stdin=open(os.path.join(self.server.prefix, 'var', 'ladderlog.txt'), 'r'), stdout=self.server.proc.stdin, stderr=open(os.path.join(self.server.prefix, 'script-error.log'), 'w'), env=mcp.common.env.get_script(), cwd=os.path.join(self.server.prefix, 'var'))

    def stop(self):
        if self.is_running():
            self.proc.terminate()
            if mcp.config.container:
                self.proc.wait()
            else:
                try:
                    self.proc.wait(5)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait()

        self.proc = None

    def is_running(self):
        return bool(self.proc and self.proc.poll() is None)

    def is_dead(self):
        return bool(self.proc and self.proc.poll())

    def is_quit(self):
        return bool(self.proc and self.proc.poll() == 0)

class Server(object):
    def __init__(self, metadata):
        self.name = metadata.server
        self.prefix = os.path.join(mcp.config.prefix, self.name)
        self.exe = os.path.join(self.prefix, 'bin', 'armagetronad-dedicated')

        self.library = metadata.library

        self.proc = None

        self.script = Script(self)

    def exists(self):
        return os.path.isfile(self.exe)

    def start(self):
        if not self.exists():
            raise mcp.error.ServerNonexistentError()

        if mcp.config.container:
            self.proc = subprocess.Popen(['/usr/local/bin/mcp-container-helper', self.prefix, os.path.join('bin', 'armagetronad-dedicated'), '--vardir', os.path.join('/', 'srv', 'var'), '--userdatadir', os.path.join('/', 'srv', 'user'), '--configdir', os.path.join('/', 'srv', 'config'), '--datadir', os.path.join('/', 'srv', 'data')], stdin=subprocess.PIPE, stdout=open(os.path.join(self.prefix, 'server.log'), 'a'), stderr=open(os.path.join(self.prefix, 'error.log'), 'w'), env=mcp.common.env.get_server(), cwd=self.prefix)
        else:
            self.proc = subprocess.Popen([os.path.join(self.prefix, 'bin', 'armagetronad-dedicated'), '--vardir', os.path.join(self.prefix, 'var'), '--userdatadir', os.path.join(self.prefix, 'user'), '--configdir', os.path.join(self.prefix, 'config'), '--datadir', os.path.join(self.prefix, 'data')], stdin=subprocess.PIPE, stdout=open(os.path.join(self.prefix, 'server.log'), 'a'), stderr=open(os.path.join(self.prefix, 'error.log'), 'w'), env=mcp.common.env.get_server(), cwd=self.prefix)

        if self.script.exists():
            self.script.start()

    def stop(self):
        self.script.stop()

        if self.is_running():
            self.proc.terminate()
            if mcp.config.container:
                self.proc.wait()
            else:
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
        return bool(self.proc and self.proc.poll() is None)

    def is_dead(self):
        return bool(self.proc and self.proc.poll())

    def is_quit(self):
        return bool(self.proc and self.proc.poll() == 0)

    def send_command(self, command):
        if not self.is_running():
            raise mcp.error.ServerStoppedError()

        self.proc.stdin.write(command.encode('latin1') + b'\n')
        self.proc.stdin.flush()

running = multiprocessing.Value('b', False)
process = None

def run():
    server_processes = {}

    for entry in mcp.model.server.items():
        server_processes[entry.server] = Server(entry)

        entry.running = entry.autostart
        entry.script_running = entry.autostart
        entry.command = ''

    try:
        while running.value:
            try:
                for entry in mcp.model.server.items():
                    # create process if necessary
                    if entry.server not in server_processes:
                        server_processes[entry.server] = Server(entry)

                        entry.running = entry.autostart
                        entry.script_running = entry.autostart
                        entry.command = ''

                    # get process
                    process = server_processes[entry.server]

                    # check if each server is supposed to be running and poll for problems
                    if entry.running:
                        if not process.proc:
                            process.start()

                        for command in entry.command.split('\n'):
                            if command:
                                process.send_command(command)

                        entry.command = ''

                        if process.is_quit():
                            process.script.stop()
                            entry.script_running = False
                            process.stop()
                            entry.running = False
                            log.warning(process.name + ' stopped by itself.')
                        elif process.is_dead():
                            with open(os.path.join(process.prefix, 'server.log'), 'a') as server_log:
                                server_log.write('WARNING: The server did not gracefully quit: now restarting.\n')
                            with open(os.path.join(process.prefix, 'error.log'), 'a') as error_log:
                                error_log.write('WARNING: The server did not gracefully quit: now restarting.\n')
                            log.warning(process.name + ' did not gracefully quit.')
                            process.stop()
                            process.start()
                            log.warning(process.name + ' restarted.')

                        if entry.script_running:
                            try:
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
                            except mcp.error.ScriptNonexistentError:
                                pass
                    else:
                        entry.script_running = False

                        if process.script.is_running():
                            process.script.stop()
                        if process.is_running():
                            process.stop()

                        # unload and reload server if necessary
                        if entry.reload:
                            del server_processes[entry.server]

                            entry.reload = False

                    entry.waiting = False

                for name in list(server_processes.keys()):
                    if not mcp.model.server.get(name):
                        del server_processes[name]

                time.sleep(mcp.config.poll_interval)
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
