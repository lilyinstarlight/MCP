import os
import sys
import time

from mcp import config, cron

mcplog = None
cmdlog = None
httplog = None

class Log(object):
	def __init__(self, log):
		if log:
			os.makedirs(os.path.dirname(log), exist_ok=True)
			self.log = open(log, 'a', 1)
		else:
			self.log = None

	def timestamp(self):
		return time.strftime('[%d/%b/%Y:%H:%M:%S %z]')

	def write(self, string):
		if self.log:
			self.log.write(string)

	def message(self, message):
		self.write(self.timestamp() + ' ' + message + '\n')

	def head(self, header):
		self.message(header)
		self.message('=' * len(header))

	def info(self, message):
		self.message('INFO: ' + message)

	def warn(self, message):
		self.message('WARN: ' + message)

	def error(self, message):
		self.message('ERROR: ' + message)

	def exception(self):
		self.error('Caught exception:\n\t' + traceback.format_exc().replace('\n', '\n\t'))

class HTTPLog(Log):
	def __init__(self, log, access_log):
		Log.__init__(self, log)

		if access_log:
			os.makedirs(os.path.dirname(log), exist_ok=True)
			self.access_log = open(log, 'a', 1)
		else:
			self.access_log = None

	def access_write(self, string):
		if self.access_log:
			self.access_log.write(string)

	def request(self, host, request, code='-', size='-', rfc931='-', authuser='-'):
		self.access_write(host + ' ' + rfc931 + ' ' + authuser + ' ' + self.timestamp() + ' "' + request + '" ' + code + ' ' + size + '\n')

mcplog = Log(config.log)
cmdlog = Log(config.cmdlog)
httplog = HTTPLog(config.httpdlog, config.accesslog)
