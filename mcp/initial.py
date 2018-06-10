import getpass
import os
import os.path

import mcp.config

import mcp.common.util

import mcp.model.user


def check():
    # create prefix directory if necessary
    try:
        os.makedirs(mcp.config.prefix)
    except FileExistsError:
        pass

    # create sources directory if necessary
    try:
        os.makedirs(mcp.config.sources)
    except FileExistsError:
        pass

    # create config directory and copy initial files if necessary
    try:
        os.makedirs(mcp.config.config)
        mcp.common.util.copy_contents(os.path.join(os.path.dirname(__file__), '/control/server'), mcp.config.config)
    except FileExistsError:
        pass

    # create config directory and copy initial files if necessary
    try:
        os.makedirs(mcp.config.scripting)
    except FileExistsError:
        pass

    # create database directory if necessary
    try:
        os.makedirs(mcp.config.database)
    except FileExistsError:
        pass

    # create log directories if necessary
    try:
        if mcp.config.log:
            os.makedirs(os.path.dirname(mcp.config.log))
    except FileExistsError:
        pass
    try:
        if mcp.config.cmdlog:
            os.makedirs(os.path.dirname(mcp.config.cmdlog))
    except FileExistsError:
        pass
    try:
        if mcp.config.httpdlog:
            os.makedirs(os.path.dirname(mcp.config.httpdlog))
    except FileExistsError:
        pass
    try:
        if mcp.config.accesslog:
            os.makedirs(os.path.dirname(mcp.config.accesslog))
    except FileExistsError:
        pass

    for user in mcp.model.user.items():
        if user.admin:
            break
    else:
        print('Setup an administrator account:')

        username = input('Username: ')
        password = getpass.getpass('Password: ')

        mcp.model.user.add(username, password, admin=True)
