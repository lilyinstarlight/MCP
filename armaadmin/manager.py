import os
import subprocess
import sys

from armaadmin import config, env, errors, log, server

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
	def __init__(self, name):
		self.name = name
		self.dir = config.prefix + '/' + name
		self.server = None
		self.script = None
		if self.exists():
			self.status_msg = 'stopped'
		else:
			self.status_msg = 'nonexistent'

	def exists(self):
		return os.path.exists(self.dir) and os.path.isdir(self.dir)

	def start(self):
		if not self.exists():
			raise errors.NoServerError

		if self.serverStatus():
			raise errors.ServerRunningError

		self.status_msg = 'starting'
		self.server = subprocess.Popen([ self.dir + '/bin/armagetronad-dedicated', '--vardir', self.dir + '/var', '--userdatadir', self.dir + '/user', '--configdir', self.dir + '/config', '--datadir', self.dir + '/data' ], stdin=subprocess.PIPE, stdout=open(self.dir + '/arma.log', 'a'), stderr=open(self.dir + '/error.log', 'w'), preexec_fn=env.demote, env=env.env, cwd=self.dir)
		self.status_msg = 'started'

		self.startScript()

	def startScript(self):
		if os.path.exists(self.dir + '/scripts/script.py') and self.serverStatus() and not self.scriptStatus():
			self.script = subprocess.Popen([ sys.executable, self.dir + '/scripts/script.py' ], stdin=open(self.dir + '/var/ladderlog.txt', 'r'), stdout=self.server.stdin, stderr=open(self.dir + '/script-error.log', 'w'), preexec_fn=env.demote, env=env.env, cwd=self.dir + '/var')

	def stop(self):
		if self.serverStatus():
			self.status_msg = 'stopping'
			self.server.terminate()
			try:
				self.server.wait(5)
			except subprocess.TimeoutExpired:
				self.server.kill()
				self.server.wait()

		self.server = None
		self.status_msg = 'stopped'

		self.stopScript()

	def stopScript(self):
		if self.scriptStatus():
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
		status = self.serverStatus()
		self.stop()
		server.create(self.name, self.getSource())
		if status:
			self.start()

	def serverStatus(self):
		if self.server:
			return self.server.poll() == None
		else:
			return False

	def scriptStatus(self):
		if self.script:
			return self.script.poll() == None
		else:
			return False

	def status(self):
		return self.status_msg

	def sendCommand(self, command):
		if self.server:
			self.server.stdin.write(command)
		else:
			raise errors.ServerStoppedError

	def getLog(self):
		with open(self.dir + '/arma.log', 'r', encoding='latin_1') as file:
			return file.read()

	def getSettings(self):
		with open(self.dir + '/config/settings_custom.cfg', 'r', encoding='latin_1') as file:
			return file.read()

	def updateSettings(self, settings):
		with open(self.dir + '/config/settings_custom.cfg', 'w', encoding='latin_1') as file:
			file.write(settings)

	def getScript(self):
		with open(self.dir + '/scripts/script.py', 'r') as file:
			return file.read()

	def updateScript(self, script):
		with open(self.dir + '/scripts/script.py', 'w') as file:
			file.write(script)

	def getScriptlog(self):
		with open(self.dir + '/script-error.log', 'r') as file:
			return file.read()

	def getSource(self):
		with open(self.dir + '/source', 'r') as file:
			return file.read().split('|')[0]

	def getRevision(self):
		with open(self.dir + '/source', 'r') as file:
			return file.read().split('|')[1]

for dir in os.listdir(config.prefix):
	if os.path.isdir(config.prefix + '/' + dir):
		servers[dir] = Server(dir)
