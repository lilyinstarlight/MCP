import os

from armaadmin import config

def handle(request):
	if config.api:
		try:
			with open(config.api + '/api.html', 'rb') as file:
				return file.read()
		except IOError:
			pass

	request.set_header('Content-Type', 'text/plain; charset=utf-8')
	return 'Sorry, there is no (documented) scripting API.'

routes = { '/api': handle }
