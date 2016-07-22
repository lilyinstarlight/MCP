import log

from mcp import config, cron


mcplog = log.Log(config.log)
cmdlog = log.Log(config.cmdlog)
httplog = log.HTTPLog(config.httpdlog, config.accesslog)
