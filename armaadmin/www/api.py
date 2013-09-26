import armaadmin.config

def handle(request):
	if config.api:
		try:
			with open(config.api + '/api.html', 'r') as file:
				return file.read()
		except IOError:
			pass

	request.set_status(404)
	request.set_header('Content-Type', 'text/plain; charset=utf-8')
	return '404 - Not Found'
