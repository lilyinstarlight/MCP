import os
import subprocess
import sys
import threading
import time

import config, env, errors, log, servers

server_list = {}

__shutdown_request = False
__is_shut_down = threading.Event()
__is_shut_down.set()

def get(server_name):
	return server_list.get(server_name)

def create(server_name, source_name, revision=None, port=0, autostart=True, users=[]):
	entry = servers.create(server_name, source_name, revision, port, autostart, users)
	server_list[entry.server] = Server(entry)

def destroy(server_name):
	if server_list.get(server_name).is_running():
		raise errors.ServerRunningError()

	servers.destroy(server_name)
	del server_list[server_name]

def poll(poll_interval=0.5):
	__is_shut_down.clear()

	load_servers()

	try:
		while not __shutdown_request:
			for server in server_list.values():
				if server.proc and not server.is_running():
					server.proc.stdout.write('WARNING: The server did not gracefully quit; now restarting.\n')
					log.mcplog.warn(server.name + ' did not gracefully quit.')
					server.stop()
					server.start()
					log.mcplog.warn(server.name + ' restarted.')

			time.sleep(poll_interval)
	finally:
		for server in server_list:
			server.stop()

		__shutdown_request = False
		__is_shut_down.set()

def start():
	threading.Thread(target=poll).start()

def stop():
	__shutdown_request = True
	__is_shut_down.wait()

def is_running():
	return not __is_shut_down.is_set()

def load_servers():
	server_list.clear()
	for entry in servers.server_db:
		server_list[entry.server] = Server(entry)

class Script(object):
	def __init__(self, server):
		self.server = server
		self.prefix = config.prefix + '/' + name
		self.exe = self.prefix + '/scripts/script.py'

		self.proc = None

	def exists(self):
		return os.path.isfile(self.exe)

	def start(self):
		if not self.exists():
			raise errors.ScriptNonExistentError()

		self.proc = subprocess.Popen([ sys.executable, self.prefix + '/scripts/script.py' ], stdin=open(self.prefix + '/var/ladderlog.txt', 'r'), stdout=self.server.proc.stdin, stderr=open(self.prefix + '/script-error.log', 'w'), preexec_fn=env.demote, env=env.env, cwd=self.prefix + '/var')

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
		return self.proc and self.proc.poll() == None

class Server(object):
	def __init__(self, metadata):
		self.name = metadata.server
		self.prefix = config.prefix + '/' + name
		self.exe = self.prefix + '/bin/armagetronad-dedicated'

		self.proc = None

		self.script = Script(self)

		if metadata.autostart:
			self.start()

	def exists(self):
		return os.path.isfile(self.exe)

	def upgrade(self, source_name=None, revision=None):
		if self.is_running():
			raise errors.ServerRunningError()

		servers.upgrade(self.name, source_name, revision)

	def modify_metadata(self, port=None, autostart=None, users=None):
		servers.modify(self.name, port, autostart, users)

	def start(self):
		if not self.exists():
			raise errors.ServerNonexistentError()

		self.proc = subprocess.Popen([ self.bin, '--vardir', self.prefix + '/var', '--userdatadir', self.prefix + '/user', '--configdir', self.prefix + '/config', '--datadir', self.prefix + '/data' ], stdin=subprocess.PIPE, stdout=open(self.prefix + '/server.log', 'a'), stderr=open(self.prefix + '/error.log', 'w'), preexec_fn=env.demote, env=env.get_user(), cwd=self.prefix)

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

	def send_command(self, command):
		if not self.is_running():
			raise errors.ServerStoppedError()

		self.proc.stdin.write(command + '\n')
