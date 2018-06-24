import os.path
import shutil
import subprocess
import sys

import mcp.config
import mcp.error

import mcp.common.cmd

def get_revision(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    with open(os.path.join(prefix, '.bzr', 'branch', 'last-revision'), 'r') as file:
        return int(file.read().split(' ', 1)[0])

def branch(library_name, url):
    prefix = os.path.join(mcp.config.scripting, library_name)

    mcp.common.cmd.head('Branching ' + library_name)

    try:
        shutil.rmtree(prefix)
    except:
        pass

    if subprocess.call(['bzr', 'branch', url, prefix], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to clone bzr tree')

def pull(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    mcp.common.cmd.head('Pulling ' + library_name)

    if subprocess.call(['bzr', 'pull'], cwd=prefix, stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to pull bzr tree')

def prepare(library_name, tmp, dst, revision=None):
    prefix = os.path.join(mcp.config.scripting, library_name)

    try:
        shutil.rmtree(dst)
    except:
        pass

    subprocess.call([sys.executable, '-m', 'virtualenv', os.path.join(tmp, 'install')], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT)

    shutil.copytree(prefix, os.path.join(tmp, 'build'))

    if revision:
        mcp.common.cmd.head('Reverting ' + library_name + ' to ' + revision)

        if subprocess.call(['bzr', 'revert', '-r' + str(revision)], cwd=os.path.join(tmp, 'build'), stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT):
            raise mcp.error.BzrError('Failed to revert bzr tree to revision')

    subprocess.call([os.path.join(dst, 'bin', 'python'), os.path.join(dst, 'build', 'setup.py'), 'install'], stdout=mcp.common.cmd.log, stderr=subprocess.STDOUT)

    shutil.copytree(os.path.join(tmp, 'install'), dst)

    shutil.rmtree(tmp)

def remove(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
