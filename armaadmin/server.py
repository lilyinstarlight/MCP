import os
import shutil
import subprocess

from armaadmin import config

def create(name, source):
	if not config.sources:
		raise NoServerCreationError

	if name in os.listdir(config.prefix):
		raise ServerExistsError

	if not source in os.listdir(config.sources):
		raise NoSourceError

	if subprocess.call([ config.sources + '/' + source + '/bootstrap.sh' ]):
		raise BuildError('Failed to bootstrap server')

	if subprocess.call([ config.sources + '/' + source + '/configure', '--enabled-dedicated', '--enable-armathentication', '--disable-automakedefaults', '--disable-sysinstall', '--disable-useradd', '--disable-etc', '--disable-desktop', '--disable-initscripts', '--disable-uninstall', '--disable-games', '--prefix="' + config.prefix + '/' + name + '"', '--localstatedir="' + config.prefix + '/' + name + '/var"' ]):
		raise BuildError('Failed to configure server')

	if subprocess.call([ 'make', '-C' + config.sources + '/' + source ]):
		raise BuildError('Failed to compile server')

	if subprocess.call([ 'make', '-C' + config.sources + '/' + source, 'install' ]):
		raise BuildError('Failed to install server')

	try:
		shutil.copytree(config.prefix + '/' + name + '/etc/armagetronad-dedicated', config.prefix + '/' + name + '/config')
	except:
		raise ConfigError('Failed to set up configuration files')

	try:
		shutil.rmtree(config.prefix + '/' + name + '/etc')
	except:
		raise ConfigError('Failed to remove "etc" directory')

	try:
		for entry in os.listdir(config.sources + '/config'):
			if os.path.isdir(config.sources + '/config/' + entry):
				shutil.copytree(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
			else:
				shutil.copy2(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
	except:
		raise ConfigError('Failed to copy configuration files')

	try:
		shutil.copytree(config.prefix + '/' + name + '/share/armagetronad-dedicated', config.prefix + '/' + name + '/data')
	except:
		raise ConfigError('Failed to set up data files')

	try:
		shutil.rmtree(config.prefix + '/' + name + '/share')
	except:
		raise ConfigError('Failed to remove "share" directory')

	if not os.path.exists(config.prefix + '/' + name + '/var'):
		try:
			os.makedirs(config.prefix + '/' + name + '/var')
		except:
			raise ConfigError('Failed to create "var" directory')

	try:
		open(config.prefix + '/' + name + '/var/ladderlog.txt', 'a').close()
	except:
		raise ConfigError('Could not ensure the existence of ladderlog.txt')

	if not os.path.exists(config.prefix + '/' + name + '/scripts'):
		try:
			os.makedirs(config.prefix + '/' + name + '/scripts')
		except:
			raise ConfigError('Could not make "scripts" directory')

	if not os.path.exists(config.prefix + '/' + name + '/user'):
		try:
			os.makedirs(config.prefix + '/' + name + '/user')
		except:
			raise ConfigError('Could not make "user" directory')

	with open(config.sources + '/' + source + '/.bzr/branch/last-revision', 'r') as file:
		revision = file.read().split(' ', 1)[0]

	with open(config.prefix + '/' + name + '/source', 'w') as file:
		file.write(source + '|' + revision)

def destroy(name):
	if not name in os.listdir(config.prefix):
		raise NoServerError

	try:
		shutil.rmtree(config.prefix + '/' + name)
	except:
		raise ConfigError('Failed to remove directory')

def updateServer(name):
	if not name in os.listdir(config.prefix):
		raise NoServerError

	with open(config.prefix + '/' + name + '/source', 'r') as file:
		source = file.read().split('|')[0]

	create(name, source)

def addSource(name, bzr):
	if not config.sources:
		raise NoServerCreationError

	if name in os.listdir(config.sources):
		raise SourceExistsError

	if subprocess.call([ 'bzr', 'branch', bzr, config.sources + '/' + source ]):
		raise BzrError('Failed to clone bzr tree')

def removeSource(name):
	if not config.sources:
		raise NoServerCreationError

	if not name in os.listdir(config.sources):
		raise NoSourceError

	try:
		shutil.rmtree(config.sources + '/' + name)
	except:
		raise ConfigError('Failed to remove directory')

def updateSource(name):
	if not config.sources:
		raise NoServerCreationError

	if not name in os.listdir(config.sources):
		raise NoSourceError

	if subprocess.call([ 'bzr', 'pull', '-d', config.sources + '/' + source ]):
		raise BzrError('Failed to pull changes')

def getSources():
	if not config.sources:
		raise NoServerCreationError

	sources = []
	for source in os.listdir(config.sources):
		if not source == 'config':
			sources.append(source)

	return sources

def getConfig():
	if not config.sources:
		raise NoServerCreationError

	with open(config.sources + '/config/server_info.cfg', 'r') as file:
		return file.read()

def updateConfig(config_text):
	if not config.sources:
		raise NoServerCreationError

	with open(config.sources + '/config/server_info.cfg', 'w') as file:
		file.write(config_text)
