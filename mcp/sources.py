import os
import re
import shutil
import subprocess

import db, errors, source

sources_allowed = re.compile('[0-9a-zA-Z-_+.]+$')

def get(source_name):
	return source_db.get(source_name)

def add(source_name, url):
	if source_db.get(source_name):
		raise errors.SourceExistsError()

	if not sources_allowed.match(source_name):
		raise errors.InvalidSourceError()

	source.branch(source_name, url)

	source_db.add(source_name, url, get_revision(source_name))

def update(source_name):
	source_obj = source_db.get(source_name)

	if not source_obj:
		raise errors.NoSourceError()

	source.pull(source_name)

	source_obj.revision = source.get_revision(source_name)

def prepare(source_name, source_dst, source_revision=None):
	if not source_db.get(source_name):
		raise errors.NoSourceError()

	source.prepare(source_name, source_dst, source_revision)

source_db = db.Database(os.path.dirname(__file__) + '/db/sources.db', [ 'source', 'url', 'revision' ])
