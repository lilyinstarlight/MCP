#!/usr/bin/env python3
import os
import re

from setuptools import setup, find_packages


name = None
version = None


def find(haystack, *needles):
    regexes = [(index, re.compile("^{}\s*=\s*'([^']*)'$".format(needle))) for index, needle in enumerate(needles)]
    values = ['' for needle in needles]

    for line in haystack:
        if len(regexes) == 0:
            break

        for rindex, (vindex, regex) in enumerate(regexes):
            match = regex.match(line)
            if match:
                values[vindex] = match.groups()[0]
                del regexes[rindex]
                break

    return values


with open(os.path.join(os.path.dirname(__file__), 'mcp', '__init__.py'), 'r') as mcp:
    name, version = find(mcp, 'name', 'version')

with open(os.path.join(os.path.dirname(__file__), 'mcp', 'config.py'), 'r') as mcp:
    sftpkey = find(mcp, 'sftpkey')


setup(
    name=name,
    version=version,
    description='a complete multi-server management framework and web interface for Armagetron Advanced',
    url='http://github.com/fkmclane/MCP',
    license='MIT',
    author='Foster McLane',
    author_email='fkmclane@gmail.com',
    install_requires=['fooster-web', 'fooster-db', 'fooster-cron', 'paramiko'],
    packages=find_packages(),
    package_data={'mcp.control': ['server/*.*', 'server/config/*.*'], 'mcp.lib': ['**/*.*'], 'mcp.page': ['html/*.*', 'res/*.*', 'res/admin/*.*', 'res/server/*.*', 'res/login/*.*', 'res/index/*.*', 'res/codemirror/*.*']},
    entry_points = {'console_scripts': ['mcp = mcp.main']},
)
