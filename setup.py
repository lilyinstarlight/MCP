#!/usr/bin/env python3
from distutils.core import setup
from distutils.command.install import install
from distutils import dir_util
from distutils import file_util
import getpass
import os
import subprocess

class post_install(install):
	def run(self):
		open('users.db', 'w').close()

		install.run(self)

		os.remove('users.db')

		print()

		import armaadmin.users

		print('Please set up the administrator account.')

		username = input('Username: ')
		password = getpass.getpass('Password: ')

		armaadmin.users.add(username, password, [], True)

		print('Making directories...')

		import armaadmin.config

		dir_util.mkpath(armaadmin.config.prefix)

		if armaadmin.config.sources:
			dir_util.copy_tree('data/sources', armaadmin.config.sources)

		if armaadmin.config.api:
			print('Installing API...')
			dir_util.copy_tree('api', armaadmin.config.api)

		response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')

		if response == "1":
			print('Installing SysV init script...')
			file_util.copy_file('dist/init/sysv/armaadmin', '/etc/init.d/')
		elif response == "2":
			print('Installing OpenRC init script...')
			file_util.copy_file('dist/init/openrc/armaadmin', '/etc/init.d/')
		elif response == "3":
			print('Installing Systemd init script...')
			file_util.copy_file('dist/init/systemd/armaadmin.service', '/usr/lib/systemd/system/')
			subprocess.call(['systemctl', 'daemon-reload'])

setup(
	name='ArmaAdmin',
	version='2.0',
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/ArmaAdmin',
	packages=[ 'armaadmin', 'armaadmin.www' ],
	package_data={ 'armaadmin': [ 'config.py', 'users.db', 'data/www/*', 'data/www/codemirror/*' ], 'armaadmin.www': [ 'data/html/*' ] },
	scripts=[ 'dist/bin/armaadmin' ],
	cmdclass={ 'install': post_install }
)
