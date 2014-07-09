import shutil

import config, errors, log

def get_revision(source_name):
	prefix = config.sources + '/' + source_name

	with open(prefix + '/.bzr/branch/last-revision', 'r') as file:
		return file.read.split(' '. 1)[0]

def branch(source_name, source_url):
	prefix = config.sources + '/' + source_name

	if subprocess.call([ 'bzr', 'branch', source_url, prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to clone bzr tree')

def pull(source_name):
	prefix = config.sources + '/' + source_name

	if subprocess.call([ 'bzr', 'pull', prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to pull bzr tree')

def prepare(source_name, source_dst, source_revision=None):
	prefix = config.sources + '/' + source_name

	shutil.copytree(prefix, source_dst)

	if source_revision:
		if subprocess.call([ 'bzr', 'revert', '-r' + source_revision, source_dst ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
			raise errors.BzrError('Failed to revert bzr tree to revision')
