import os
import pwd

import config

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

if config.scripting:
	if env.get('PYTHONPATH'):
		env['PYTHONPATH'] += ':' + config.scripting
	else:
		env['PYTHONPATH'] = config.scripting
