import os
import re
import shutil
import subprocess

from armaadmin import config, errors, log

sources = {}

sources_allowed = re.compile('[0-9a-zA-Z-_+]+$')

def get(name):
	if not name in sources:
		raise errors.NoSourceError

	return sources[name]

def add(name, bzr):
	if not config.creation:
		raise errors.NoServerCreationError

	if name in sources:
		raise errors.SourceExistsError

	if not sources_allowed.match(name):
		raise errors.InvalidSourceError

	if subprocess.call([ 'bzr', 'branch', bzr, config.sources + '/' + name ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
		raise errors.BzrError('Failed to clone bzr tree')

	sources[name] = Source(name)

def remove(name):
	if not config.creation:
		raise errors.NoServerCreationError

	if not name in sources:
		raise errors.NoSourceError

	try:
		shutil.rmtree(config.sources + '/' + name)
	except:
		raise errors.ConfigError('Failed to remove directory')

	del sources[name]

def getConfig():
	if not config.creation:
		raise errors.NoServerCreationError

	with open(config.config + '/server_info.cfg', 'r', encoding='latin_1') as file:
		return file.read()

def updateConfig(config_text):
	if not config.creation:
		raise errors.NoServerCreationError

	with open(config.config + '/server_info.cfg', 'w', encoding='latin_1') as file:
		file.write(config_text)

class Source:
	def __init__(self, name):
		self.name = name
		self.dir = config.sources + '/' + name

	def update(self):
		if subprocess.call([ 'bzr', 'pull', '-d', config.sources + '/' + self.name ], stdout=log.cmdlog, stderr=subprocess.STDOUT):
			raise errors.BzrError('Failed to pull changes')

	def getRevision(self):
		with open(self.dir + '/.bzr/branch/last-revision', 'r') as file:
			return file.read().split(' ', 1)[0]

for dir in os.listdir(config.sources):
	if os.path.isdir(config.sources + '/' + dir):
		sources[dir] = Source(dir)
