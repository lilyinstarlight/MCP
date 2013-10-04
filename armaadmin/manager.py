import os
import pwd
import subprocess
import sys

import armaadmin.config
import armaadmin.server

servers = {}

def get(name):
	return servers.get(name)

def create(name):
	if name in servers:
		return 'Server already exists'

	result = server.create(name)
	if result == 'success':
		servers[name] = Server(name)

	return result

def destroy(name):
	if not name in servers:
		return 'Server does not exist'

	servers[name].stop()
	result = server.destroy(name)
	if result == 'success':
		del servers[name]

	return result

def poll():
	for server in servers.values():
		if server.server and not server.serverStatus():
			server.server.stdout.write('WARNING: The server did not gracefully quit; now restarting.\n')
			server.stop()
			server.start()

def demote():
	if config.user:
		os.setgid(passwd.pw_gid)
		os.setuid(passwd.pw_uid)

class Server:
	def __init__(self, name):
		self.dir = config.prefix + '/' + name
		self.server = None
		self.script = None
		if self.exists():
			self.status_msg = 'stopped'
		else:
			self.status_msg = 'nonexistent'

	def exists(self):
		return os.path.exists(self.dir)

	def start(self):
		if self.exists() and not self.serverStatus():
			self.status_msg = 'starting'
			self.server = subprocess.Popen([ self.dir + '/bin/armagetronad-dedicated', '--vardir', self.dir + '/var', '--userdatadir', self.dir + '/user', '--configdir', self.dir + '/config', '--datadir', self.dir + '/data' ], stdin=subprocess.PIPE, stdout=open(self.dir + '/arma.log', 'a'), stderr=open(self.dir + '/error.log', 'w'), preexec_fn=demote, env=env, cwd=self.dir)
			self.status_msg = 'started'

			self.startScript()

	def startScript(self):
		if os.path.exists(self.dir + '/scripts/script.py') and self.serverStatus() and not self.scriptStatus():
			self.script = subprocess.Popen([ sys.executable, self.dir + '/scripts/script.py' ], stdin=open(self.dir + '/var/ladderlog.txt', 'r'), stdout=self.server.stdin, stderr=open(self.dir + '/script-error.log', 'w'), preexec_fn=demote, env=env, cwd=self.dir + '/var')

	def stop(self):
		if self.serverStatus():
			self.status_msg = 'stopping'
			self.server.terminate()
			try:
				self.server.wait(5)
			except TimeoutExpired:
				self.server.kill()
				self.server.wait()

		self.server = None
		self.status_msg = 'stopped'

		self.stopScript()

	def stopScript(self):
		if self.scriptStatus():
			self.server.terminate()
			try:
				self.server.wait(5)
			except TimeoutExpired:
				self.server.kill()
				self.server.wait()

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

	def getLog(self):
		with open(self.dir + '/arma.log', 'r') as file:
			return file.read()

	def getScriptlog(self):
		with open(self.dir + '/script-error.log', 'r') as file:
			return file.read()

	def getSettings(self):
		with open(self.dir + '/config/settings_custom.cfg', 'r') as file:
			return file.read()

	def getScript(self):
		with open(self.dir + '/scripts/script.py', 'r') as file:
			return file.read()

	def updateSettings(self, settings):
		with open(self.dir + '/config/settings_custom.cfg', 'w') as file:
			file.write(settings)

	def updateScript(self, script):
		with open(self.dir + '/scripts/script.py', 'w') as file:
			file.write(script)

env = os.environ.copy()

if config.user:
	passwd = pwd.getpwnam(config.user)
	env['HOME'] = passwd.pw_dir
	env['LOGNAME'] = passwd.pw_name
	env['USER'] = passwd.pw_name

if config.api:
	if env.get('PYTHONPATH'):
		env['PYTHONPATH'] += ':' + config.api
	else:
		env['PYTHONPATH'] = config.api

for dir in os.listdir(config.prefix):
	if os.path.isdir(os.path.join(config.prefix, dir)):
		servers[dir] = Server(dir)
