import os
import pwd

from armaadmin import config

def demote():
	if config.user:
		os.setgid(passwd.pw_gid)
		os.setuid(passwd.pw_uid)

env = os.environ.copy()

if config.user:
	passwd = pwd.getpwnam(config.user)
	env['HOME'] = passwd.pw_dir
	env['LOGNAME'] = passwd.pw_name
	env['USER'] = passwd.pw_name

if config.api:
	if env.get('PYTHONPATH'):
		env['PYTHONPATH'] += ':' + config.api
	else:
		env['PYTHONPATH'] = config.api
