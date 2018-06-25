import os
import os.path

import mcp.config


base_env = os.environ.copy()


def get_user():
    return os.getuid(), os.getgid()


def get_env():
    return base_env


def get_server():
    server_env = base_env.copy()

    return server_env


def get_script():
    script_env = get_env().copy()

    return script_env


def get_build(dst):
    build_env = get_env().copy()

    build_env['DESTDIR'] = dst

    return build_env
