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
    tmp = mcp.config.tmp + '/' + server_name
    tmp_build = tmp + '/build'
    tmp_install = tmp + '/install'

    mcp.control.source.prepare(source_name, tmp_build, revision)

    # build
    mcp.common.cmd.head('Building ' + server_name)

    if subprocess.call([shlex.quote('./bootstrap.sh')], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to bootstrap server')

    if subprocess.call([shlex.quote('./configure') + ' --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix=' + shlex.quote(prefix) + ' --localstatedir=' + shlex.quote(prefix + '/var')], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, shell=True):
        raise mcp.error.BuildError('Failed to configure server')

    if subprocess.call(['make'], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build):
        raise mcp.error.BuildError('Failed to compile server')

    if subprocess.call(['make', 'install'], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT, cwd=tmp_build, env=mcp.common.env.get_build(tmp_install)):
        raise mcp.error.BuildError('Failed to install server')

    # configure
    mcp.common.cmd.head('Configuring ' + server_name)

    try:
        mcp.common.util.copy_contents(tmp_install + prefix + '/etc/armagetronad-dedicated', tmp_install + prefix + '/config')
        mcp.common.util.copy_contents(tmp_install + prefix + '/share/armagetronad-dedicated', tmp_install + prefix + '/data')
    except:
        raise mcp.error.ConfigError('Failed to move data files')

    try:
        shutil.rmtree(tmp_install + prefix + '/etc')
        shutil.rmtree(tmp_install + prefix + '/share')
    except:
        raise mcp.error.ConfigError('Failed to remove unnecessary directories')

    try:
        os.makedirs(tmp_install + prefix + '/var', exist_ok=True)
        os.makedirs(tmp_install + prefix + '/scripts', exist_ok=True)
        os.makedirs(tmp_install + prefix + '/user', exist_ok=True)
        os.makedirs(tmp_install + prefix + '/log', exist_ok=True)
    except:
        raise mcp.error.ConfigError('Failed to create necessary directories')

    try:
        with open(tmp_install + prefix + '/config/settings_custom.cfg', 'a') as file:
            pass
        with open(tmp_install + prefix + '/config/server_port.cfg', 'a') as file:
            pass
        with open(tmp_install + prefix + '/var/ladderlog.txt', 'a') as file:
            pass
        with open(tmp_install + prefix + '/server.log', 'a') as file:
            pass
        with open(tmp_install + prefix + '/error.log', 'a') as file:
            pass
        with open(tmp_install + prefix + '/script-error.log', 'a') as file:
            pass
    except:
        raise mcp.error.ConfigError('Failed to create necessary files')

    try:
        mcp.common.util.copy_contents(mcp.config.config, tmp_install + prefix + '/config')
    except:
        raise mcp.error.ConfigError('Failed to copy custom configuration files')

    # merge
    mcp.common.cmd.head('Merging ' + server_name)

    try:
        mcp.common.util.copy_contents(tmp_install + prefix, prefix)
    except:
        raise mcp.error.MergeError('Failed to copy server')

    try:
        shutil.rmtree(tmp)
    except:
        raise mcp.error.MergeError('Failed to remove build directory')

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
