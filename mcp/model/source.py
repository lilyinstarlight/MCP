import os
import re
import shutil
import subprocess

import fooster.db

import mcp.config
import mcp.error

import mcp.control.source

sources_allowed = '[0-9a-zA-Z-_+.]+'

def items():
    return iter(source_db)

def get(source_name):
    return source_db.get(source_name)

def add(source_name, url):
    if not re.match('^' + sources_allowed + '$', source_name):
        raise mcp.error.InvalidSourceError()

    if source_name in source_db:
        raise mcp.error.SourceExistsError()

    mcp.control.source.branch(source_name, url)

    return source_db.add(source_name, url, mcp.control.source.get_revision(source_name))

def update(source_name):
    if source_name not in source_db:
        raise mcp.error.NoSourceError()

    mcp.control.source.pull(source_name)

    source_db[source_name].revision = mcp.control.source.get_revision(source_name)

def prepare(source_name, dst, revision=None):
    if source_name not in source_db:
        raise mcp.error.NoSourceError()

    mcp.control.source.prepare(source_name, dst, revision)

def remove(source_name):
    if source_name not in source_db:
        raise mcp.error.NoSourceError()

    mcp.control.source.remove(source_name)

    del source_db[source_name]

source_db = fooster.db.Database(mcp.config.database + '/db/sources.db', ['source', 'url', 'revision'])
