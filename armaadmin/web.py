import http.server
import os
import threading
import urllib

from armaadmin import config

server = None

def init(routes):
	global server

	server = HTTPServer(config.address, config.port, routes, config.log)
	threading.Thread(target=server.serve_forever).start()

def destroy():
	global server

	server.shutdown()
	server.server_close()
	server = None

class HTTPServer(http.server.HTTPServer):
	def __init__(self, address, port, routes, log=None):
		self.routes = routes

		if log:
			os.makedirs(os.path.dirname(log), exist_ok=True)
			self.log = open(log, 'a', 1)
		else:
			self.log = None

		super(HTTPServer, self).__init__((address, port), self.makeHandler())
		self.log.write('Serving HTTP on ' + self.server_name + ' port ' + str(self.server_port) + '...\n')

	def server_close(self):
		if self.log:
			self.log.close()
		self.socket.close()

	def makeHandler(self):
		class HTTPHandler(http.server.BaseHTTPRequestHandler):
			def parse_url_params(args, params):
				for arg in params.split('&'):
					if '=' in arg:
						value = arg.split('=', 1)
						args[urllib.parse.unquote_plus(value[0])] = urllib.parse.unquote_plus(value[1])
					else:
						args[urllib.parse.unquote_plus(arg)] = None

			def do_HEAD(self):
				request = self.path.split('?', 1)
				self.request = request[0]
				self.get_args = {}
				if len(request) > 1:
					HTTPHandler.parse_url_params(self.get_args, request[1])

				self.args = self.get_args.copy()
				if hasattr(self, 'post_args'):
					self.args.update(self.post_args)
				else:
					self.post_args = {}

				self.cookies = {}
				cookies = self.headers.get('cookie')
				if cookies:
					entries = cookies.split('; ')
					for cookie in entries:
						value = cookie.split('=', 1)
						self.cookies[value[0]] = value[1]

				self.output_headers = {}
				self.set_header('Content-Type', 'text/html; charset=utf-8')
				if self.request in self.routes:
					self.set_status(200)
					self.response = self.routes[self.request](self).encode('utf-8')
				elif '404' in self.routes:
					self.set_status(404)
					self.response = self.routes['404'](self).encode('utf-8')
				else:
					self.set_status(404)
					self.set_header('Content-Type', 'text/plain; charset=utf-8')
					self.response = '404 - Not Found'.encode('utf-8')
				self.set_header('Content-Length', len(self.response))

				self.send_response(self.status)
				for header in self.output_headers:
					self.send_header(header, self.output_headers[header])
				self.end_headers()

			def do_GET(self):
				self.do_HEAD()
				self.wfile.write(self.response)

			def do_POST(self):
				if self.headers.get('content-type') == 'application/x-www-form-urlencoded':
					post = self.rfile.readline(self.headers.get('content-length', -1))
					self.post_args = {}
					HTTPHandler.parse_url_params(self.post_args, post)

				self.do_GET()

			def log_message(self, format, *args):
				if self.log:
					self.log.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

			def set_status(self, code):
				self.status = code

			def set_header(self, header, value):
				self.output_headers[header] = value

			def set_cookie(self, values, time=24):
				self.set_header('Set-Cookie', '; '.join('%s=%s' % (k, v) for k, v in values.items()) + '; Max-Age=' + str(time * 3600))

		HTTPHandler.routes = self.routes
		HTTPHandler.log = self.log
		return HTTPHandler
