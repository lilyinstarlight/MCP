import os
import shlex
import shutil
import subprocess

from armaadmin import config, errors

def create(name, source):
	if not config.sources:
		raise errors.NoServerCreationError

	if name in os.listdir(config.prefix):
		raise errors.ServerExistsError

	if source == 'config':
		raise errors.InvalidSourceError

	if not source in os.listdir(config.sources):
		raise errors.NoSourceError

	if subprocess.call([ shlex.quote(config.sources + '/' + source + '/bootstrap.sh') ], cwd=config.sources + '/' + source, shell=True):
		raise errors.BuildError('Failed to bootstrap server')

	if subprocess.call([ shlex.quote(config.sources + '/' + source + '/configure') + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(config.prefix + '/' + name) + ' --localstatedir=' + shlex.quote(config.prefix + '/' + name + '/var') ], cwd=config.sources + '/' + source, shell=True):
		raise errors.BuildError('Failed to configure server')

	if subprocess.call([ 'make', '-C' + shlex.quote(config.sources + '/' + source) ], cwd=config.sources + '/' + source):
		raise errors.BuildError('Failed to compile server')

	if subprocess.call([ 'make', '-C' + shlex.quote(config.sources + '/' + source), 'install' ], cwd=config.sources + '/' + source):
		raise errors.BuildError('Failed to install server')

	try:
		shutil.copytree(config.prefix + '/' + name + '/etc/armagetronad-dedicated', config.prefix + '/' + name + '/config')
	except:
		raise errors.ConfigError('Failed to set up configuration files')

	try:
		shutil.rmtree(config.prefix + '/' + name + '/etc')
	except:
		raise errors.ConfigError('Failed to remove "etc" directory')

	try:
		for entry in os.listdir(config.sources + '/config'):
			if os.path.isdir(config.sources + '/config/' + entry):
				shutil.copytree(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
			else:
				shutil.copy2(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
	except:
		raise errors.ConfigError('Failed to copy configuration files')

	try:
		shutil.copytree(config.prefix + '/' + name + '/share/armagetronad-dedicated', config.prefix + '/' + name + '/data')
	except:
		raise errors.ConfigError('Failed to set up data files')

	try:
		shutil.rmtree(config.prefix + '/' + name + '/share')
	except:
		raise errors.ConfigError('Failed to remove "share" directory')

	if not os.path.exists(config.prefix + '/' + name + '/var'):
		try:
			os.makedirs(config.prefix + '/' + name + '/var')
		except:
			raise errors.ConfigError('Failed to create "var" directory')

	try:
		open(config.prefix + '/' + name + '/var/ladderlog.txt', 'a').close()
	except:
		raise errors.ConfigError('Could not ensure the existence of ladderlog.txt')

	if not os.path.exists(config.prefix + '/' + name + '/scripts'):
		try:
			os.makedirs(config.prefix + '/' + name + '/scripts')
		except:
			raise errors.ConfigError('Could not make "scripts" directory')

	if not os.path.exists(config.prefix + '/' + name + '/user'):
		try:
			os.makedirs(config.prefix + '/' + name + '/user')
		except:
			raise errors.ConfigError('Could not make "user" directory')

	with open(config.prefix + '/' + name + '/source', 'w') as file:
		file.write(source + '|' + getSourceRevision(source))

def destroy(name):
	if not name in os.listdir(config.prefix):
		raise errors.NoServerError

	try:
		shutil.rmtree(config.prefix + '/' + name)
	except:
		raise errors.ConfigError('Failed to remove directory')

def upgrade(name):
	if not name in os.listdir(config.prefix):
		raise errors.NoServerError

	create(name, getServerSource(name))

def getSource(name):
	with open(config.prefix + '/' + name + '/source', 'r') as file:
		return file.read().split('|')[0]

def getRevision(name):
	with open(config.prefix + '/' + name + '/source', 'r') as file:
		return file.read().split('|')[1]

def addSource(name, bzr):
	if not config.sources:
		raise errors.NoServerCreationError

	if name == 'config':
		raise errors.InvalidSourceError

	if name in os.listdir(config.sources):
		raise errors.SourceExistsError

	if subprocess.call([ 'bzr', 'branch', bzr, config.sources + '/' + name ]):
		raise errors.BzrError('Failed to clone bzr tree')

def removeSource(name):
	if not config.sources:
		raise errors.NoServerCreationError

	if name == 'config':
		raise errors.InvalidSourceError

	if not name in os.listdir(config.sources):
		raise errors.NoSourceError

	try:
		shutil.rmtree(config.sources + '/' + name)
	except:
		raise errors.ConfigError('Failed to remove directory')

def updateSource(name):
	if not config.sources:
		raise errors.NoServerCreationError

	if name == 'config':
		raise errors.InvalidSourceError

	if not name in os.listdir(config.sources):
		raise errors.NoSourceError

	if subprocess.call([ 'bzr', 'pull', '-d', config.sources + '/' + name ]):
		raise errors.BzrError('Failed to pull changes')

def getSourceRevision(name):
	if not config.sources:
		raise errors.NoServerCreationError

	if name == 'config':
		raise errors.InvalidSourceError

	with open(config.sources + '/' + name + '/.bzr/branch/last-revision', 'r') as file:
		return file.read().split(' ', 1)[0]

def getSources():
	if not config.sources:
		raise errors.NoServerCreationError

	sources = []
	for source in os.listdir(config.sources):
		if not source == 'config':
			sources.append(source)

	return sources

def getConfig():
	if not config.sources:
		raise errors.NoServerCreationError

	with open(config.sources + '/config/server_info.cfg', 'r') as file:
		return file.read()

def updateConfig(config_text):
	if not config.sources:
		raise errors.NoServerCreationError

	with open(config.sources + '/config/server_info.cfg', 'w') as file:
		file.write(config_text)
