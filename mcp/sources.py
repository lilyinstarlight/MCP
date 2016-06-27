import os
import re
import shutil
import subprocess

from mcp import db, errors, source

sources_allowed = '[0-9a-zA-Z-_+.]+'

def get(source_name):
    return source_db.get(source_name)

def add(source_name, url):
    if not re.match('^' + sources_allowed + '$', source_name):
        raise errors.InvalidSourceError()

    if source_db.get(source_name):
        raise errors.SourceExistsError()

    source.branch(source_name, url)

    return source_db.add(source_name, url, get_revision(source_name))

def update(source_name):
    source_obj = source_db.get(source_name)

    if not source_obj:
        raise errors.NoSourceError()

    source.pull(source_name)

    source_obj.revision = source.get_revision(source_name)

def prepare(source_name, dst, revision=None):
    if not source_db.get(source_name):
        raise errors.NoSourceError()

    source.prepare(source_name, dst, revision)

def remove(source_name):
    if not source_db.get(source_name):
        raise errors.NoSourceError()

    source.remove(source_name)

source_db = db.Database(config.database + '/db/sources.db', ['source', 'url', 'revision'])
