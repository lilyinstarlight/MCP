import os
import shlex
import shutil
import subprocess

import config, env, errors, log, source

def copy_contents(src, dst):
	for entry in os.listdir(src):
		entry = src + '/' + entry
		if os.path.isdir(entry):
			copy_contents(entry, dst + '/' + entry)
		else:
			shutil.copy2(entry, dst + '/' + entry)

def chown_contents(path, uid, gid):
	for entry in os.listdir(path):
		entry = path + '/' + entry
		if os.path.isdir(entry):
			chown_contents(entry, uid, gid)
		else:
			os.chown(entry, uid, gid)

def build(server_name, source_name, source_revision=None):
	if not config.creation:
		raise errors.NoServerCreationError()

	prefix = config.prefix + '/' + server_name
	tmp_build = config.tmp + '/' + server_name + '/build'
	tmp_install = config.tmp + '/' + server_name + '/install'

	source.prepare(source_name, tmp_build)

	#Build
	message = 'Building ' + name
	log.cmdlog.write(message + '\n' + '=' * len(message))

	if subprocess.call([ shlex.quote(tmp_build + '/bootstrap.sh') ], stdout=log.cmdlog, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
		raise errors.BuildError('Failed to bootstrap server')

	if subprocess.call([ shlex.quote(tmp_build + '/configure') + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(prefix) + ' --localstatedir=' + shlex.quote(prefix + '/var') ], stdout=log.cmdlog, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
		raise errors.BuildError('Failed to configure server')

	if subprocess.call([ 'make', '-C' + shlex.quote(tmp_build) ], stdout=log.cmdlog, stderr=subprocess.STDOUT, cwd=tmp_build):
		raise errors.BuildError('Failed to compile server')

	if subprocess.call([ 'make', '-C' + shlex.quote(tmp_build), 'install' ], stdout=log.cmdlog, stderr=subprocess.STDOUT, cwd=tmp_build, env=env.build_env(tmp_install)):
		raise errors.BuildError('Failed to install server')

	#Configure
	message = 'Configuring ' + name
	log.cmdlog.write(message + '\n' + '=' * len(message))

	try:
		copy_contents(prefix + '/etc/armagetronad-dedicated', prefix + '/config')
	except:
		raise errors.ConfigError('Failed to move configuration files')

	try:
		shutil.rmtree(prefix + '/etc')
	except:
		raise errors.ConfigError('Failed to remove "etc" directory')

	try:
		copy_contents(config.config, prefix + '/config')
	except:
		raise errors.ConfigError('Failed to copy custom configuration files')

	try:
		copy_contents(prefix + '/share/armagetronad-dedicated', prefix + '/data')
	except:
		raise errors.ConfigError('Failed to move data files')

	try:
		shutil.rmtree(prefix + '/share')
	except:
		raise errors.ConfigError('Failed to remove "share" directory')

	try:
		os.makedirs(prefix + '/var', exist_ok=True)
	except:
		raise errors.ConfigError('Failed to create "var" directory')

	try:
		with open(prefix + '/config/settings_custom.cfg', 'a') as file:
			pass

		with open(prefix + '/var/ladderlog.txt', 'a') as file:
			pass
	except:
		raise errors.ConfigError('Failed to create necessary files')

	try:
		os.makedirs(prefix + '/scripts', exist_ok=True)
	except:
		raise errors.ConfigError('Failed to create "scripts" directory')

	try:
		os.makedirs(prefix + '/user', exist_ok=True)
	except:
		raise errors.ConfigError('Failed to create "user" directory')

	#Merge
	message = 'Merging ' + name
	log.cmdlog.write(message + '\n' + '=' * len(message))

	try:
		copy_contents(tmp_install, prefix)
	except:
		raise errors.MergeError('Failed to copy server')

	if env.passwd:
		try:
			chown_contents(prefix + '/config', env.passwd.pw_uid, env.passwd.pw_gid)
			chown_contents(prefix + '/data', env.passwd.pw_uid, env.passwd.pw_gid)
			chown_contents(prefix + '/scripts', env.passwd.pw_uid, env.passwd.pw_gid)
			chown_contents(prefix + '/user', env.passwd.pw_uid, env.passwd.pw_gid)
			chown_contents(prefix + '/var', env.passwd.pw_uid, env.passwd.pw_gid)
		except:
			raise errors.MergeError('Failed to set permissions')

def destroy(server_name):
	prefix = config.prefix + '/' + server_name

	try:
		shutil.rmtree(prefix)
	except:
		raise errors.ConfigError('Failed to remove directory')
