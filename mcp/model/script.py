import os
import re
import shutil
import subprocess

import fooster.db

import mcp.config
import mcp.error

import mcp.control.script


libraries_allowed = '[0-9a-zA-Z-_+.]+'


def items():
    return iter(library_db)

def get(library_name):
    return library_db.get(library_name)

def add(library_name, url):
    if not re.match('^' + libraries_allowed + '$', library_name):
        raise mcp.error.InvalidLibraryError()

    if library_name in library_db:
        raise mcp.error.LibraryExistsError()

    mcp.control.script.branch(library_name, url)

    return library_db.add(library_name, url, get_revision(library_name))

def update(library_name):
    if library_name not in library_db:
        raise mcp.error.NoLibraryError()

    mcp.control.script.pull(library_name)

    library_db[library_name].revision = mcp.control.script.get_revision(library_name)

def prepare(library_name, dst, revision=None):
    if library_name not in library_db:
        raise mcp.error.NoLibraryError()

    mcp.control.script.prepare(library_name, dst, revision)

def remove(library_name):
    if library_name not in library_db:
        raise mcp.error.NoLibraryError()

    mcp.control.script.remove(library_name)

    del library_db[library_name]

def doc_get(library_name):
    if library_name not in library_db:
        raise mcp.error.NoLibraryError()

    try:
        with open(os.path.join(mcp.config.scripting, library_name, 'doc.html'), 'r') as doc:
            return doc.read()
    except FileNotFoundError:
        return ''

library_db = fooster.db.Database(mcp.config.database + '/libraries.db', ['library', 'url', 'revision'])
