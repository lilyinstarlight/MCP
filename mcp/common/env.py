import os
import os.path

import mcp.config


base_env = os.environ.copy()


def get_env():
    return base_env


def get_server():
    server_env = base_env.copy()

    return server_env


def get_script(library):
    script_env = get_env().copy()

    script_env['PYTHONPATH'] = os.path.join(mcp.config.scripting, library)

    return script_env


def get_build(dst):
    build_env = get_env().copy()

    build_env['DESTDIR'] = dst

    return build_env
