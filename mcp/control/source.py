import logging
import shutil
import subprocess

import mcp.config
import mcp.error

import mcp.common.cmd

def get_revision(source_name):
    prefix = mcp.config.sources + '/' + source_name

    with open(prefix + '/.bzr/branch/last-revision', 'r') as file:
        return int(file.read().split(' ', 1)[0])

def branch(source_name, url):
    prefix = mcp.config.sources + '/' + source_name

    mcp.common.cmd.head('Branching ' + source_name)

    try:
        shutil.rmtree(prefix)
    except:
        pass

    if subprocess.call(['bzr', 'branch', url, prefix], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to clone bzr tree')

def pull(source_name):
    prefix = mcp.config.sources + '/' + source_name

    mcp.common.cmd.head('Pulling ' + source_name)

    if subprocess.call(['bzr', 'pull'], cwd=prefix, stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to pull bzr tree')

def prepare(source_name, dst, revision=None):
    prefix = mcp.config.sources + '/' + source_name

    try:
        shutil.rmtree(dst)
    except:
        pass

    shutil.copytree(prefix, dst)

    if revision:
        mcp.common.cmd.head('Reverting ' + source_name + ' to ' + revision)

        if subprocess.call(['bzr', 'revert', '-r' + revision], cwd=dst, stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
            raise mcp.error.BzrError('Failed to revert bzr tree to revision')

def remove(source_name):
    prefix = mcp.config.sources + '/' + source_name

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
