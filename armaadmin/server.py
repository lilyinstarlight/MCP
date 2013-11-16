import os
import re
import shlex
import shutil
import subprocess

from armaadmin import config, errors, sources

server_allowed = re.compile('[0-9a-zA-Z-_]+$')

def create(name, source_name):
	if not config.creation:
		raise errors.NoServerCreationError

	if not server_allowed.match(name):
		raise errors.InvalidServerError

	source = sources.get(source_name)

	if subprocess.call([ shlex.quote(source.dir + '/bootstrap.sh') ], cwd=source.dir, shell=True):
		raise errors.BuildError('Failed to bootstrap server')

	if subprocess.call([ shlex.quote(source.dir + '/configure') + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(config.prefix + '/' + name) + ' --localstatedir=' + shlex.quote(config.prefix + '/' + name + '/var') ], cwd=source.dir, shell=True):
		raise errors.BuildError('Failed to configure server')

	if subprocess.call([ 'make', '-C' + shlex.quote(source.dir) ], cwd=source.dir):
		raise errors.BuildError('Failed to compile server')

	if subprocess.call([ 'make', '-C' + shlex.quote(source.dir), 'install' ], cwd=source.dir):
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
		for entry in os.listdir(config.config):
			entry = config.config + entry
			if os.path.isdir(entry):
				shutil.copytree(entry, config.prefix + '/' + name + '/config')
			else:
				shutil.copy2(entry, config.prefix + '/' + name + '/config')
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
		file.write(source.name + '|' + source.getRevision())

def destroy(name):
	if not name in os.listdir(config.prefix) or not os.path.isdir(config.prefix + '/' + name):
		raise errors.NoServerError

	try:
		shutil.rmtree(config.prefix + '/' + name)
	except:
		raise errors.ConfigError('Failed to remove directory')
