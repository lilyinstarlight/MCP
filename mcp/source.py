import shutil

import config, errors, log, sources

def branch(source_name, source_url):
	prefix = config.sources + '/' + source_name

	if subprocess.call([ 'bzr', 'branch', source_url, prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to clone bzr tree')

def pull(source_name):
	if not sources.get(source_name):
		raise errors.NoSourceError()

	prefix = config.sources + '/' + source_name

	if subprocess.call([ 'bzr', 'pull', prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to pull bzr tree')

def prepare(source_name, source_dst, source_revision=None):
	source = sources.get(source_name)

	if not source:
		raise errors.NoSourceError()

	if not source_revision:
		source_revision = source.revision
	elif source_revision > source.revision:
		raise errors.InvalidSourceRevisionError()

	shutil.copytree(config.sources + '/' + source_name, source_dst)

	if subprocess.call([ 'bzr', 'revert', '-r' + source_revision, source_dst ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to revert bzr tree to revision')
