import os
import subprocess
import sys

import config, env, errors, log, server

servers = {}

def get(name):
	if not name in servers:
		raise errors.NoServerError

	return servers[name]

def create(name, source):
	if name in servers:
		raise errors.ServerExistsError

	server.create(name, source)
	servers[name] = Server(name)

def destroy(name):
	if not name in servers:
		raise errors.NoServerError

	servers[name].stop()
	server.destroy(name)
	del servers[name]

def poll():
	for server in servers.values():
		if server.server and not server.serverStatus():
			server.server.stdout.write('WARNING: The server did not gracefully quit; now restarting.\n')
			server.stop()
			server.start()
			log.warn(server.name + ' did not gracefully quit and was restarted.')

class Server:
	def __init__(self, name, dir):
		self.name = name
		self.dir = dir
		self.bin = self.dir + '/bin/armagetronad-dedicated'
		self.server = None
		self.script = None
		if self.exists():
			self.status_msg = 'stopped'
		else:
			self.status_msg = 'nonexistent'

	def exists(self):
		return os.path.isfile(self.bin) and os.access(self.bin, os.X_OK)

	def start(self):
		if not self.exists():
			raise errors.NoServerError()

		if self.server_status():
			return

		self.status_msg = 'starting'
		self.server = subprocess.Popen([ self.bin, '--vardir', self.dir + '/var', '--userdatadir', self.dir + '/user', '--configdir', self.dir + '/config', '--datadir', self.dir + '/data' ], stdin=subprocess.PIPE, stdout=open(self.dir + '/server.log', 'a'), stderr=open(self.dir + '/error.log', 'w'), preexec_fn=env.demote, env=env.env, cwd=self.dir)
		self.status_msg = 'started'

		self.start_script()

	def start_script(self):
		if os.path.exists(self.dir + '/scripts/script.py') and self.serverStatus() and not self.scriptStatus():
			self.script = subprocess.Popen([ sys.executable, self.dir + '/scripts/script.py' ], stdin=open(self.dir + '/var/ladderlog.txt', 'r'), stdout=self.server.stdin, stderr=open(self.dir + '/script-error.log', 'w'), preexec_fn=env.demote, env=env.env, cwd=self.dir + '/var')

	def stop(self):
		if self.server_status():
			self.status_msg = 'stopping'
			self.server.terminate()
			try:
				self.server.wait(5)
			except subprocess.TimeoutExpired:
				self.server.kill()
				self.server.wait()

		self.server = None
		self.status_msg = 'stopped'

		self.stop_script()

	def stop_script(self):
		if self.script_status():
			self.script.terminate()
			try:
				self.script.wait(5)
			except subprocess.TimeoutExpired:
				self.script.kill()
				self.script.wait()

		self.script = None

	def restart(self):
		self.stop()
		self.start()

	def reload(self):
		if self.server:
			self.server.stdin.write('INCLUDE settings.cfg')
			self.server.stdin.write('INCLUDE server_info.cfg')
			self.server.stdin.write('INCLUDE settings_custom.cfg')
			if self.script:
				self.server.stdin.write('INCLUDE script.cfg')
		else:
			raise errors.ServerStoppedError

	def upgrade(self):
		status = self.server_status()
		self.stop()
		server.create(self.name, self.getSource())
		if status:
			self.start()

	def server_status(self):
		if self.server:
			return self.server.poll() == None
		else:
			return False

	def script_status(self):
		if self.script:
			return self.script.poll() == None
		else:
			return False

	def status(self):
		return self.status_msg

	def send_command(self, command):
		if self.server:
			self.server.stdin.write(command)
		else:
			raise errors.ServerStoppedError()

	def get_log(self):
		with open(self.dir + '/arma.log', 'r', encoding='latin_1') as file:
			return file.read()

	def get_settings(self):
		with open(self.dir + '/config/settings_custom.cfg', 'r', encoding='latin_1') as file:
			return file.read()

	def update_settings(self, settings):
		with open(self.dir + '/config/settings_custom.cfg', 'w', encoding='latin_1') as file:
			file.write(settings)

	def get_script(self):
		with open(self.dir + '/scripts/script.py', 'r') as file:
			return file.read()

	def update_script(self, script):
		with open(self.dir + '/scripts/script.py', 'w') as file:
			file.write(script)

	def get_scriptlog(self):
		with open(self.dir + '/script-error.log', 'r') as file:
			return file.read()

for dir in os.listdir(config.prefix):
	temp = Server(dir)
	if temp.exists():
		servers[dir] = temp
