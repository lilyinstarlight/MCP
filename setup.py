#!/usr/bin/env python3
import sys

if sys.version_info < (3, 3):
    print('Only Python 3.3 or later is supported')
    sys.exit(1)

from distutils.core import setup
from distutils.command.install import install
from distutils import dir_util
from distutils import file_util
import getpass
import os
import shutil
import subprocess

import config

from .mcp import name, version

def setupUser():
	import mcp.users

	print()
	print('Please set up the administrator account.')

	username = input('Username: ')
	password = getpass.getpass('Password: ')

	mcp.users.add(username, password, [], True)

def setupDirs():
	print()
	print('Making directories...')

	dir_util.mkpath(config.prefix)

	if config.creation:
		dir_util.mkpath(config.sources)
		dir_util.copy_tree('config', config.config)

def setupScripting():
	if config.scripting:
		print()
		print('Installing scripting library...')
		dir_util.copy_tree('scripting', config.scripting)

def setupInit():
	print()
	response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')

	if response == "1":
		print()
		print('Installing SysV init script...')
		file_util.copy_file('init/sysv/mcp', '/etc/init.d/')
	elif response == "2":
		print()
		print('Installing OpenRC init script...')
		file_util.copy_file('init/openrc/mcp', '/etc/init.d/')
	elif response == "3":
		print()
		print('Installing Systemd init script...')
		file_util.copy_file('init/systemd/mcp.service', '/usr/lib/systemd/system/')
		subprocess.call(['systemctl', 'daemon-reload'])

class cmd_install(install):
	def run(self):
		open('mcp/users.db', 'w').close()
		setupUser()

		print()
		print('Installing...')

		shutil.copy('config.py', 'mcp/')
		install.run(self)
		os.remove('mcp/config.py')

		os.remove('mcp/users.db')

		setupDirs()
		setupScripting()
		setupInit()

class cmd_upgrade(install):
	def run(self):
		print()
		print('Upgrading...')

		shutil.copy('config.py', 'mcp/')
		install.run(self)
		os.remove('mcp/config.py')

		setupScripting()
		setupInit()

setup(
	name=name,
	version=version,
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/MCP',
	license='MIT',
	packages=[ 'mcp', 'mcp.routes' ],
	package_data={ 'mcp': [ 'config.py', 'users.db', 'www/*.*', 'www/admin/*.*', 'www/codemirror/*.*' ], 'mcp.routes': [ 'html/*.*' ] },
	scripts=[ 'bin/mcp' ],
	cmdclass={ 'install': cmd_install, 'upgrade': cmd_upgrade }
)
