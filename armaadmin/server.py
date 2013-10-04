import os
import shutil
import subprocess

import armaadmin.config

def create(name, source):
	if not config.sources:
		return 'Server creation disabled'

	if name in os.listdir(config.prefix):
		return 'Server already exists'

	if not source in os.listdir(config.sources):
		return 'Sources do not exist'

	if subprocess.call([ config.sources + '/' + source + '/bootstrap.sh' ]):
		return 'Failed to bootstrap server'

	if subprocess.call([ config.sources + '/' + source + '/configure', '--enabled-dedicated', '--enable-armathentication', '--disable-automakedefaults', '--disable-sysinstall', '--disable-useradd', '--disable-etc', '--disable-desktop', '--disable-initscripts', '--disable-uninstall', '--disable-games', '--prefix="' + config.prefix + '/' + name + '"', '--localstatedir="' + config.prefix + '/' + name + '/var"' ]):
		return 'Failed to configure server'

	if subprocess.call([ 'make', '-C' + config.sources + '/' + source ]):
		return 'Failed to compile server'

	if subprocess.call([ 'make', '-C' + config.sources + '/' + source, 'install' ]):
		return 'Failed to install server'

	try:
		shutil.copytree(config.prefix + '/' + name + '/etc/armagetronad-dedicated', config.prefix + '/' + name + '/config')
	except:
		return 'Failed to set up configuration files'

	try:
		shutil.rmtree(config.prefix + '/' + name + '/etc')
	except:
		return 'Failed to remove "etc" directory'

	try:
		for entry in os.listdir(config.sources + '/config'):
			if os.path.isdir(config.sources + '/config/' + entry):
				shutil.copytree(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
			else:
				shutil.copy2(config.sources + '/config/' + entry, config.prefix + '/' + name + '/config')
	except:
		return 'Failed to copy configuration files'

	try:
		shutil.copytree(config.prefix + '/' + name + '/share/armagetronad-dedicated', config.prefix + '/' + name + '/data')
	except:
		return 'Failed to set up data files'

	try:
		shutil.rmtree(config.prefix + '/' + name + '/share')
	except:
		return 'Failed to remove "share" directory'

	if not os.path.exists(config.prefix + '/' + name + '/var'):
		try:
			os.makedirs(config.prefix + '/' + name + '/var')
		except:
			return 'Could not make "var" directory'

	try:
		open(config.prefix + '/' + name + '/var/ladderlog.txt', 'a').close()
		open(config.prefix + '/' + name + '/var/input.txt', 'a').close()
	except:
		return 'Could not ensure the existence of ladderlog.txt and input.txt'

	if not os.path.exists(config.prefix + '/' + name + '/scripts'):
		try:
			os.makedirs(config.prefix + '/' + name + '/scripts')
		except:
			return 'Could not make "scripts" directory'

	if not os.path.exists(config.prefix + '/' + name + '/user'):
		try:
			os.makedirs(config.prefix + '/' + name + '/user')
		except:
			return 'Could not make "user" directory'

	return 'success'

def destroy(name):
	if not name in os.listdir(config.prefix):
		return 'Server does not exist'

	try:
		shutil.rmtree(config.prefix + '/' + name)
	except:
		return 'Failed to remove directory'

		return 'sucess'
