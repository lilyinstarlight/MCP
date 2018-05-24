import os
import os.path

from mcp import config

from mcp.common import util


def check():
    try:
        os.mkdirs(config.prefix)
    except FileExistsError:
        pass

    try:
        os.mkdirs(config.sources)
    except FileExistsError:
        pass

    try:
        os.mkdirs(config.config)
        util.copy_contents(os.path.join(__file__, 'control/server'), config.config)
    except FileExistsError:
        pass

    try:
        os.mkdirs(config.scripting)
        util.copy_contents(os.path.join(__file__, 'control/script'), config.scripting)
    except FileExistsError:
        pass

    try:
        os.mkdirs(config.database)
    except FileExistsError:
        pass

    try:
        os.mkdirs(os.path.dirname(config.log))
    except FileExistsError:
        pass

    try:
        os.mkdirs(os.path.dirname(config.cmdlog))
    except FileExistsError:
        pass

    try:
        os.mkdirs(os.path.dirname(config.httpdlog))
    except FileExistsError:
        pass

    try:
        os.mkdirs(os.path.dirname(config.accesslog))
    except FileExistsError:
        pass
