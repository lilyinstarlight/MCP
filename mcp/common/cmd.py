from mcp import config


log = open(config.cmdlog, 'a')


def head(header):
    log.write('\n')
    log.write(header)
    log.write('\n')
    log.write('-'*len(header))
    log.write('\n')
