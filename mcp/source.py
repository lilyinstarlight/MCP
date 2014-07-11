import shutil

import config, errors, log

def get_revision(source_name):
	prefix = config.sources + '/' + source_name

	with open(prefix + '/.bzr/branch/last-revision', 'r') as file:
		return file.read.split(' '. 1)[0]

def branch(source_name, url):
	prefix = config.sources + '/' + source_name

	message = 'Branching ' + source_name
	log.cmdlog.message(message)
	log.cmdlog.message('=' * len(message))

	if subprocess.call([ 'bzr', 'branch', url, prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to clone bzr tree')

def pull(source_name):
	prefix = config.sources + '/' + source_name

	message = 'Pulling ' + source_name
	log.cmdlog.message(message)
	log.cmdlog.message('=' * len(message))

	if subprocess.call([ 'bzr', 'pull', prefix ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to pull bzr tree')

def prepare(source_name, dst, revision=None):
	prefix = config.sources + '/' + source_name

	shutil.copytree(prefix, dst)

	if revision:
		message = 'Reverting ' + source_name + ' to ' + revision
		log.cmdlog.message(message)
		log.cmdlog.message('=' * len(message))

		if subprocess.call([ 'bzr', 'revert', '-r' + revision, dst ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
			raise errors.BzrError('Failed to revert bzr tree to revision')

def remove(source_name):
	prefix = config.sources + '/' + source_name

	try:
		shutil.rmtree(prefix)
	except:
		raise errors.ConfigError('Failed to remove directory')
