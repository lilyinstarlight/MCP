import os
import pwd

import config

user_env = os.environ.copy()
passwd = None

def demote():
	if config.user:
		os.setgid(passwd.pw_gid)
		os.setuid(passwd.pw_uid)
def get_script():
	script_env = user_env.copy()

	if config.scripting:
		if script_env.get('PYTHONPATH'):
			script_env['PYTHONPATH'] += ':' + config.scripting
		else:
			script_env['PYTHONPATH'] = config.scripting

	return script_env

def get_build(dst):
	build_env = os.environ.copy()

	build_env['DESTDIR'] = dst

	return build_env

if config.user:
	passwd = pwd.getpwnam(config.user)
	user_env['HOME'] = passwd.pw_dir
	user_env['LOGNAME'] = passwd.pw_name
	user_env['USER'] = passwd.pw_name
