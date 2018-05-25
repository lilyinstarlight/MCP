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

def build(server_name, source_name, revision=None):
    if not mcp.config.creation:
        raise mcp.error.NoServerCreationError()

    prefix = mcp.config.prefix + '/' + server_name
    tmp_build = mcp.config.tmp + '/' + server_name + '/build'
    tmp_install = mcp.config.tmp + '/' + server_name + '/install'

    mcp.control.source.prepare(source_name, tmp_build, revision)

    # build
    cmd.head('Building ' + server_name)

    if subprocess.call([shlex.quote(tmp_build + '/bootstrap.sh')], stdout=cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to bootstrap server')

    if subprocess.call([shlex.quote(tmp_build + '/configure') + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(prefix) + ' --localstatedir=' + shlex.quote(prefix + '/var')], stdout=cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to configure server')

    if subprocess.call(['make', '-C' + tmp_build], stdout=cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build):
        raise mcp.error.BuildError('Failed to compile server')

    if subprocess.call(['make', '-C' + tmp_build, 'install'], stdout=cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, env=env.get_build(tmp_install)):
        raise mcp.error.BuildError('Failed to install server')

    # configure
    cmd.head('Configuring ' + server_name)

    try:
        util.copy_contents(prefix + '/etc/armagetronad-dedicated', prefix + '/config')
        util.copy_contents(prefix + '/share/armagetronad-dedicated', prefix + '/data')
    except:
        raise mcp.error.ConfigError('Failed to move data files')

    try:
        shutil.rmtree(prefix + '/etc')
        shutil.rmtree(prefix + '/share')
    except:
        raise mcp.error.ConfigError('Failed to remove unnecessary directories')

    try:
        os.makedirs(prefix + '/var', exist_ok=True)
        os.makedirs(prefix + '/scripts', exist_ok=True)
        os.makedirs(prefix + '/user', exist_ok=True)
        os.makedirs(prefix + '/log', exist_ok=True)
    except:
        raise mcp.error.ConfigError('Failed to create necessary directories')

    try:
        with open(prefix + '/config/settings_custom.cfg', 'a') as file:
            pass
        with open(prefix + '/config/server_port.cfg', 'a') as file:
            pass
        with open(prefix + '/var/ladderlog.txt', 'a') as file:
            pass
        with open(prefix + '/server.log', 'a') as file:
            pass
        with open(prefix + '/error.log', 'a') as file:
            pass
        with open(prefix + '/script-error.log', 'a') as file:
            pass
    except:
        raise mcp.error.ConfigError('Failed to create necessary files')

    try:
        util.copy_contents(mcp.config.config, prefix + '/config')
    except:
        raise mcp.error.ConfigError('Failed to copy custom configuration files')

    # merge
    cmd.head('Merging ' + server_name)

    try:
        util.copy_contents(tmp_install, prefix)
    except:
        raise mcp.error.MergeError('Failed to copy server')

def set_port(server_name, port):
    prefix = mcp.config.prefix + '/' + server_name

    with open(prefix + '/config/server_port.cfg', 'w') as file:
        if port:
            file.write('SERVER_PORT ' + str(port) + '\n')

def destroy(server_name):
    prefix = mcp.config.prefix + '/' + server_name

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
