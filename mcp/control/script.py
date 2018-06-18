import shutil

import mcp.config
import mcp.error

def get_revision(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    with open(os.path.join(prefix, '.bzr', 'branch', 'last-revision'), 'r') as file:
        return int(file.read.split(' ', 1)[0])

def branch(library_name, url):
    prefix = os.path.join(mcp.config.scripting, library_name)

    cmd.head('Branching ' + library_name)

    try:
        shutil.rmtree(prefix)
    except:
        pass

    if subprocess.call(['bzr', 'branch', url, prefix], stdout=cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to clone bzr tree')

def pull(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    cmd.head('Pulling ' + library_name)

    if subprocess.call(['bzr', 'pull', prefix], stdout=cmd.log, stderr=subprocess.STDOUT):
        raise mcp.error.BzrError('Failed to pull bzr tree')

def prepare(library_name, dst, revision=None):
    prefix = os.path.join(mcp.config.scripting, library_name)

    try:
        shutil.rmtree(dst)
    except:
        pass

    shutil.copytree(prefix, dst)

    if revision:
        cmd.head('Reverting ' + library_name + ' to ' + revision)

        if subprocess.call(['bzr', 'revert', '-r' + revision, dst], stdout=cmd.log, stderr=subprocess.STDOUT):
            raise mcp.error.BzrError('Failed to revert bzr tree to revision')

def remove(library_name):
    prefix = os.path.join(mcp.config.scripting, library_name)

    try:
        shutil.rmtree(prefix)
    except:
        raise mcp.error.ConfigError('Failed to remove directory')
