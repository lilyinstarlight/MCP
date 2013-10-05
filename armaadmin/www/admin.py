from armaadmin import sessions

def handle(request):
	session = sessions.get(request.cookies.get('session'))
	if not session or not session.user.admin:
		request.set_status(307)
		request.set_header('Location', '/')
		return ''

	with open(os.path.dirname(__file__) + '/data/html/admin.html', 'r') as file:
		return file.read()
