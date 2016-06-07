import os
import pwd

from mcp import config

base_env = os.environ.copy()

user_env = base_env.copy()
passwd = None

def demote():
    if config.user:
        os.setgid(passwd.pw_gid)
        os.setuid(passwd.pw_uid)

def get_env():
    return base_env

def get_user():
    return user_env

def get_script():
    script_env = get_user().copy()

    if config.scripting:
        if script_env.get('PYTHONPATH'):
            script_env['PYTHONPATH'] += ':' + config.scripting
        else:
            script_env['PYTHONPATH'] = config.scripting

    return script_env

def get_build(dst):
    build_env = get_env().copy()

    build_env['DESTDIR'] = dst

    return build_env

if config.user:
    passwd = pwd.getpwnam(config.user)
    user_env['HOME'] = passwd.pw_dir
    user_env['LOGNAME'] = passwd.pw_name
    user_env['USER'] = passwd.pw_name
