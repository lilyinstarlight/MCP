#!/usr/bin/env python3
from distutils.core import setup
from distutils.command.install import install
from distutils import dir_util
from distutils import file_util
import getpass
import os
import shutil
import subprocess

import config

def setupUser():
	import armaadmin.users

	print()
	print('Please set up the administrator account.')

	username = input('Username: ')
	password = getpass.getpass('Password: ')

	armaadmin.users.add(username, password, [], True)

def setupDirs():
	print()
	print('Making directories...')

	dir_util.mkpath(config.prefix)

	if config.creation:
		dir_util.mkpath(config.sources)
		dir_util.copy_tree('config', config.config)

def setupApi():
	if config.api:
		print()
		print('Installing API...')
		dir_util.copy_tree('api', config.api)

def setupInit():
	response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')

	if response == "1":
		print()
		print('Installing SysV init script...')
		file_util.copy_file('init/sysv/armaadmin', '/etc/init.d/')
	elif response == "2":
		print()
		print('Installing OpenRC init script...')
		file_util.copy_file('init/openrc/armaadmin', '/etc/init.d/')
	elif response == "3":
		print()
		print('Installing Systemd init script...')
		file_util.copy_file('init/systemd/armaadmin.service', '/usr/lib/systemd/system/')
		subprocess.call(['systemctl', 'daemon-reload'])

class post_install(install):
	def run(self):
		open('armaadmin/users.db', 'w').close()
		setupUser()

		print()
		print('Installing...')

		shutil.copy('config.py', 'armaadmin/')
		install.run(self)
		os.remove('armaadmin/config.py')

		os.remove('armaadmin/users.db')

		setupDirs()
		setupApi()
		setupInit()

class upgrade(install):
	def run(self):
		print()
		print('Upgrading...')

		shutil.copy('config.py', 'armaadmin/')
		install.run(self)
		os.remove('armaadmin/config.py')

		setupApi()
		setupInit()

setup(	name='ArmaAdmin',
	version='2.0',
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/ArmaAdmin',
	license='MIT',
	packages=[ 'armaadmin', 'armaadmin.routes' ],
	package_data={ 'armaadmin': [ 'config.py', 'users.db', 'www/*.*', 'www/admin/*.*', 'www/codemirror/*.*' ], 'armaadmin.routes': [ 'html/*.*' ] },
	scripts=[ 'bin/armaadmin' ],
	cmdclass={ 'install': post_install, 'upgrade': upgrade }
)
