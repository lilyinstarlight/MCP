#!/usr/bin/env python3
from distutils.core import setup

from mcp import name, version

setup(
    name=name,
    version=version,
    description='a complete multi-server management framework and web interface for Armagetron Advanced',
    author='Foster McLane',
    author_email='fkmclane@gmail.com',
    url='http://github.com/fkmclane/MCP',
    license='MIT',
    packages=['mcp', 'mcp.api', 'mcp.control', 'mcp.lib', 'mcp.model', 'mcp.page'],
    package_data={'mcp': ['../config.py', 'config/*.*', 'scripting/*.*'], 'mcp.page': ['html/*.*', 'res/*.*', 'res/admin/*.*', 'res/server/*.*', 'res/login/*.*', 'res/codemirror/*.*']},
    scripts=['bin/mcp'],
)
