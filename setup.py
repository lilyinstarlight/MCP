#!/usr/bin/env python3
import sys

if sys.version_info < (3, 3):
	print('Only Python 3.3 or later is supported')
	sys.exit(1)

from distutils.core import setup
from distutils.command.install import install
from distutils import dir_util
from distutils import file_util
from getpass import getpass
import os
import shutil
import subprocess

import config

from mcp import name, version

def configure_dirs():
	dir_util.mkpath(config.prefix)

	if config.creation:
		dir_util.mkpath(config.sources)
		dir_util.copy_tree('config', config.config)

def configure_scripting():
	if config.scripting:
		dir_util.copy_tree('scripting', config.scripting)

def configure_init():
	print()
	response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')
	print()

	if response == "1":
		file_util.copy_file('service/sysv/mcp', '/etc/init.d/')
	elif response == "2":
		file_util.copy_file('service/openrc/mcp', '/etc/init.d/')
	elif response == "3":
		file_util.copy_file('service/systemd/mcp.service', '/usr/lib/systemd/system/')
		subprocess.call(['systemctl', 'daemon-reload'])

def configure_user():
	import mcp.users

	#Look for at least one user with admin status
	for user in mcp.users.user_db:
		if user.admin:
			break
	#If user not found
	else:
		print()
		print('Please set up an administrator account.')

		username = input('Username: ')
		password = getpass('Password: ')

		mcp.users.add(username, password, admin=True)

def configure():
		print()
		print('Configuring...')

		configure_dirs()
		configure_scripting()
		configure_init()

		configure_user()

class cmd_install(install):
	def run(self):
		install.run(self)
		configure()

setup(
	name=name,
	version=version,
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/MCP',
	license='MIT',
	packages=[ 'mcp', 'mcp.interface' ],
	package_data={ 'mcp': [ '../config.py' ], 'mcp.routes': [ 'html/*.*', 'res/*.*', 'res/admin/*.*', 'res/server/*.*', 'res/login/*.*', 'res/codemirror/*.*' ] },
	scripts=[ 'bin/mcp' ],
	cmdclass={ 'install': cmd_install }
)
