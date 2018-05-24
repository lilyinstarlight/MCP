import sys

from mcp import config


if config.cmdlog:
    log = open(config.cmdlog, 'a')
else:
    log = sys.stdout


def head(header):
    log.write('\n')
    log.write(header)
    log.write('\n')
    log.write('-'*len(header))
    log.write('\n')
