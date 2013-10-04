#!/usr/bin/env python3
import distutils.core
import getpass
import os
import shutil
import subprocess

import config

open('armaadmin/users.db', 'w').close()

import armaadmin.users

print('Please set up the administrator account.')

username = input('Username: ')
password = getpass.getpass('Password: ')

print('Setting configuration...')

armaadmin.users.add(username, password, [], True)
shutil.copy('config.py', 'armaadmin')

print('Installing...')

distutils.core.setup(
	name='ArmaAdmin',
	version='2.0',
	description='A complete Armagetron Advanced multi-server management framework and web interface',
	author='Foster McLane',
	author_email='fkmclane@gmail.com',
	url='http://github.com/fkmclane/ArmaAdmin',
	packages=[ 'armaadmin', 'armaadmin.www' ],
	package_data={ 'armaadmin': [ 'users.db', 'data/www' ], 'armaadmin.www': [ 'data/html' ] },
	scripts=[ 'dist/bin/armaadmin' ],
)

os.remove('armaadmin/config.py')
os.remove('armaadmin/users.db')

print('Making directories...')

os.makedirs(config.prefix, exist_ok=True)

if config.sources:
	shutil.copytree('sources', config.sources, copy_function=shutil.copy)

if config.api:
	print('Installing API...')
	shutil.copytree('api', config.api, copy_function=shutil.copy)

response = input('Which init system are you using: [1] SysV (Debian, Ubuntu, CentOS), [2] OpenRC (Gentoo), [3] Systemd (Arch, Fedora), [*] Other/None? ')

print('Installing init script...')

if response == "1":
	shutil.copy('dist/init/sysv/armaadmin', '/etc/init.d/')
elif response == "2":
	shutil.copy('dist/init/openrc/armaadmin', '/etc/init.d/')
elif response == "3":
	shutil.copy('dist/init/systemd/armaadmin.service', '/usr/lib/systemd/system/')
	subprocess.call(['systemctl', 'daemon-reload'])

print('Done.')
