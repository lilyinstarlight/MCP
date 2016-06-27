import os

from mcp import config

base_env = os.environ.copy()

server_env = base_env.copy()

def get_env():
    return base_env

def get_server():
    return server_env

def get_script():
    script_env = get_server().copy()

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
