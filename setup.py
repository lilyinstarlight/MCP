#!/usr/bin/env python3
from distutils.core import setup
from distutils.command.install import install
import getpass
import os
import shutil
import subprocess

class post_install(install):
	def run(self):
		open('users.db', 'w').close()

		install.run(self)

		os.remove('users.db')

		import armaadmin.users

		print('Please set up the administrator account.')

		username = input('Username: ')
		password = getpass.getpass('Password: ')

		armaadmin.users.add(username, password, [], True)

		print('Making directories...')

		import armaadmin.config

		os.makedirs(config.prefix, exist_ok=True)

		if config.sources:
			shutil.copytree('sources', config.sources, copy_function=shutil.copy)

		if config.api:
			print('Installing API...')
			shutil.copytree('api', config.api, copy_function=shutil.copy)

		response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')

		if response == "1":
			print('Installing SysV init script...')
			shutil.copy('dist/init/sysv/armaadmin', '/etc/init.d/')
		elif response == "2":
			print('Installing OpenRC init script...')
			shutil.copy('dist/init/openrc/armaadmin', '/etc/init.d/')
		elif response == "3":
			print('Installing Systemd init script...')
			shutil.copy('dist/init/systemd/armaadmin.service', '/usr/lib/systemd/system/')
			subprocess.call(['systemctl', 'daemon-reload'])

setup(
	name='ArmaAdmin',
	version='2.0',
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/ArmaAdmin',
	packages=[ 'armaadmin', 'armaadmin.www' ],
	package_data={ 'armaadmin': [ 'config.py', 'users.db', 'data/www' ], 'armaadmin.www': [ 'data/html' ] },
	scripts=[ 'dist/bin/armaadmin' ],
	cmdclass={ 'install': post_install }
)
