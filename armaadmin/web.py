import http.server
import json
import time
import os
import re
import socketserver
import sys
import threading
import urllib

server = None

def init(address, port, routes, log):
	global server

	server = HTTPServer(address, port, routes, log)
	threading.Thread(target=server.serve_forever).start()

def destroy():
	global server

	server.shutdown()
	server.server_close()
	server = None

class HTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	errors = [ '404', '500' ]

	def __init__(self, address, port, routes, log=None):
		self.routes = {}
		self.error_routes = {}
		for route in routes:
			if route in HTTPServer.errors:
				self.error_routes[route] = routes[route]
			else:
				self.routes[re.compile('^' + route + '$')] = routes[route];

		self.log = log

		super(HTTPServer, self).__init__((address, port), self.makeHandler())
		self.log.write('Serving HTTP on ' + self.server_name + ' port ' + str(self.server_port) + '...\n')

	def server_close(self):
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

				try:
					self.match = None
					for regex in self.routes:
						self.match = regex.match(self.request)
						if self.match:
							self.regex = regex
							break

					if self.match:
						self.set_status(200)
						self.response = self.routes[self.regex](self)
					else:
						self.set_status(404)
						if '404' in self.error_routes:
							self.response = self.error_routes['404'](self)
						else:
							self.set_header('Content-Type', 'text/plain; charset=utf-8')
							self.response = '404 - Not Found'
				except:
					type, value, traceback = sys.exc_info()
					self.log_message('Caught %s while accessing "%s": %s', type.__name__, self.request, value)

					self.set_status(500)
					if '500' in self.error_routes:
						self.response = self.error_routes['500'](self)
					else:
						self.set_header('Content-Type', 'text/plain; charset=utf-8')
						self.response = '500 - Internal Server Error'

				if not isinstance(self.response, bytes):
					self.response = self.response.encode('utf-8')

				self.set_header('Content-Length', len(self.response))

				self.send_response(self.status)
				for header in self.output_headers:
					self.send_header(header, self.output_headers[header])
				self.end_headers()

			def do_GET(self):
				self.do_HEAD()
				self.wfile.write(self.response)

			def do_POST(self):
				post = self.rfile.readline(int(self.headers.get('content-length', '-1'))).decode('utf-8')
				content_type = self.headers.get('content-type')
				if content_type == 'application/x-www-form-urlencoded':
					self.post_args = {}
					HTTPHandler.parse_url_params(self.post_args, post)
				elif content_type == 'multipart/form-data':
					pass
				elif content_type == 'application/json':
					self.json_data = json.loads(post)

				self.do_GET()

			def log_message(self, format, *args):
				if self.log:
					self.log.write('[%s] %s\n' % (time.strftime('%Y/%m/%d %H:%M:%S'), format % args))

			def set_status(self, code):
				self.status = code

			def set_header(self, header, value):
				self.output_headers[header] = value

			def set_cookie(self, values, time=24):
				self.set_header('Set-Cookie', '; '.join('%s=%s' % (k, v) for k, v in values.items()) + '; Max-Age=' + str(time * 3600))

		HTTPHandler.routes = self.routes
		HTTPHandler.error_routes = self.error_routes
		HTTPHandler.log = self.log
		return HTTPHandler
