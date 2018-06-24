import sys

import mcp.config


if mcp.config.cmdlog:
    log = open(mcp.config.cmdlog, 'a')
else:
    log = sys.stdout


def head(header):
    log.write('\n')
    log.write(header)
    log.write('\n')
    log.write('-'*len(header))
    log.write('\n')
    log.flush()
