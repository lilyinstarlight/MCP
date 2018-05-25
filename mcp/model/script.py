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

    if library_db.get(library_name):
        raise mcp.error.LibraryExistsError()

    mcp.control.script.branch(library_name, url)

    return library_db.add(library_name, url, get_revision(library_name))

def update(library_name):
    library_obj = library_db.get(library_name)

    if not library_obj:
        raise mcp.error.NoLibraryError()

    mcp.control.script.pull(library_name)

    library_obj.revision = mcp.control.script.get_revision(library_name)

def prepare(library_name, dst, revision=None):
    if not library_db.get(library_name):
        raise mcp.error.NoLibraryError()

    mcp.control.script.prepare(library_name, dst, revision)

def remove(library_name):
    if not library_db.get(library_name):
        raise mcp.error.NoLibraryError()

    mcp.control.script.remove(library_name)

library_db = fooster.db.Database(mcp.config.database + '/db/libraries.db', ['library', 'url', 'revision'])
