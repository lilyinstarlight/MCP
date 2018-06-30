import os
import shlex
import shutil
import subprocess

import mcp.config
import mcp.error

import mcp.common.cmd
import mcp.common.env
import mcp.common.util

import mcp.control.source

def build(server_name, source_name, library_name=None, source_revision=None, library_revision=None):
    if not mcp.config.creation:
        raise mcp.error.NoServerCreationError()

    if mcp.config.container:
        prefix = os.path.join('/', 'srv')
    else:
        prefix = os.path.join(mcp.config.prefix, server_name)

    tmp = os.path.join(mcp.config.tmp, server_name)
    tmp_source = os.path.join(tmp, 'source')
    tmp_library = os.path.join(tmp, 'library')
    tmp_build = os.path.join(tmp, 'build')
    tmp_install = os.path.join(tmp, 'install')
    if prefix[0] == '/':
        tmp_prefix = os.path.join(tmp, 'install', prefix[1:])
    else:
        tmp_prefix = os.path.join(tmp, 'install', prefix)

    mcp.control.source.prepare(source_name, tmp_source, tmp_build, source_revision)

    # build
    mcp.common.cmd.head('Building ' + server_name)

    if subprocess.call([shlex.quote(os.path.join('.', 'bootstrap.sh'))], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to bootstrap server')

    if subprocess.call([shlex.quote(os.path.join('.', 'configure')) + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(prefix) + ' --localstatedir=' + shlex.quote(os.path.join(prefix, 'var'))], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to configure server')

    if subprocess.call(['make'], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build):
        raise mcp.error.BuildError('Failed to compile server')

    if subprocess.call(['make', 'install'], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, env=mcp.common.env.get_build(tmp_install)):
        raise mcp.error.BuildError('Failed to install server')

    # configure
    mcp.common.cmd.head('Configuring ' + server_name)

    try:
        mcp.common.util.copy_contents(os.path.join(tmp_prefix, 'etc', 'armagetronad-dedicated'), os.path.join(tmp_prefix, 'config'))
        mcp.common.util.copy_contents(os.path.join(tmp_prefix, 'share', 'armagetronad-dedicated'), os.path.join(tmp_prefix, 'data'))
    except:
        raise mcp.error.ConfigError('Failed to move data files')

    try:
        shutil.rmtree(os.path.join(tmp_prefix, 'etc'))
        shutil.rmtree(os.path.join(tmp_prefix, 'share'))
    except:
        raise mcp.error.ConfigError('Failed to remove unnecessary directories')

    try:
        os.makedirs(os.path.join(tmp_prefix, 'var'), exist_ok=True)
        os.makedirs(os.path.join(tmp_prefix, 'user'), exist_ok=True)
        os.makedirs(os.path.join(tmp_prefix, 'log'), exist_ok=True)
    except:
        raise mcp.error.ConfigError('Failed to create necessary directories')

    try:
        if library_name:
            mcp.control.script.prepare(library_name, tmp_library, os.path.join(tmp_prefix, 'script'), library_revision)
        else:
            os.makedirs(os.path.join(tmp_prefix, 'script'), exist_ok=True)
    except:
        raise mcp.error.ConfigError('Failed to create script directory')

    try:
        with open(os.path.join(tmp_prefix, 'config', 'settings_custom.cfg'), 'a') as file:
            pass
        with open(os.path.join(tmp_prefix, 'config', 'server_port.cfg'), 'a') as file:
            pass
        with open(os.path.join(tmp_prefix, 'var', 'ladderlog.txt'), 'a') as file:
            pass
        with open(os.path.join(tmp_prefix, 'server.log'), 'a') as file:
            pass
        with open(os.path.join(tmp_prefix, 'error.log'), 'a') as file:
            pass
        with open(os.path.join(tmp_prefix, 'script-error.log'), 'a') as file:
            pass
    except:
        raise mcp.error.ConfigError('Failed to create necessary files')

    try:
        mcp.common.util.copy_contents(mcp.config.config, os.path.join(tmp_prefix, 'config'))
    except:
        raise mcp.error.ConfigError('Failed to copy custom configuration files')

    # merge
    mcp.common.cmd.head('Merging ' + server_name)

    try:
        mcp.common.util.copy_contents(tmp_prefix, os.path.join(mcp.config.prefix, server_name))
    except:
        raise mcp.error.MergeError('Failed to copy server')

    try:
        shutil.rmtree(tmp)
    except:
        raise mcp.error.MergeError('Failed to remove build directory')

def set_port(server_name, port):
    prefix = os.path.join(mcp.config.prefix, server_name)

    with open(os.path.join(prefix, 'config', 'server_port.cfg'), 'w') as file:
        if port:
            file.write('SERVER_PORT ' + str(port) + '\n')

def destroy(server_name):
    prefix = os.path.join(mcp.config.prefix, server_name)

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
