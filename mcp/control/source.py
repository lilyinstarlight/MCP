import logging
import os.path
import shutil
import subprocess

import mcp.config
import mcp.error

import mcp.common.cmd

def get_revision(source_name):
    prefix = os.path.join(mcp.config.sources, source_name)

    with open(os.path.join(prefix, '.bzr', 'branch', 'last-revision'), 'r') as file:
        return int(file.read().split(' ', 1)[0])

def branch(source_name, url):
    prefix = os.path.join(mcp.config.sources, source_name)

    mcp.common.cmd.head('Branching ' + source_name)

    try:
        shutil.rmtree(prefix)
    except:
        pass

    if subprocess.call(['bzr', 'branch', url, prefix], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to clone bzr tree')

def pull(source_name):
    prefix = os.path.join(mcp.config.sources, source_name)

    mcp.common.cmd.head('Pulling ' + source_name)

    if subprocess.call(['bzr', 'pull'], cwd=prefix, stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to pull bzr tree')

def prepare(source_name, tmp, dst, revision=None):
    prefix = os.path.join(mcp.config.sources, source_name)

    try:
        shutil.rmtree(tmp)
    except:
        pass

    try:
        shutil.rmtree(dst)
    except:
        pass

    shutil.copytree(prefix, tmp)

    if revision:
        mcp.common.cmd.head('Reverting ' + source_name + ' to ' + str(revision))

        if subprocess.call(['bzr', 'revert', '-r' + str(revision)], cwd=tmp, stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
            raise mcp.error.BzrError('Failed to revert bzr tree to revision')

    shutil.copytree(tmp, dst)

    shutil.rmtree(tmp)

def remove(source_name):
    prefix = os.path.join(mcp.config.sources, source_name)

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
