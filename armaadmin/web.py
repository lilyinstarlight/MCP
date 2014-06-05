import re
import socket
import socketserver
import ssl
import time
import threading

#Server details
server_version = 'web.py/0.1'
http_version = 'HTTP/1.1'
http_encoding = 'iso-8859-1'
default_encoding = 'utf-8'

#Constraints
max_request_size = 4096
max_line_size = 1024
max_headers = 64

#Standard HTTP status messages
status_messages = {
	#1xx Informational
	100: 'Continue',
	101: 'Switching Protocols',
	102: 'Processing',

	#2xx Success
	200: 'OK',
	201: 'Created',
	202: 'Accepted',
	203: 'Non-Authoritative Information',
	204: 'No Content',
	205: 'Reset Content',
	206: 'Partial Content',
	207: 'Multi-Status',
	208: 'Already Reported',
	226: 'IM Used',

	#3xx Redirection
	300: 'Multiple Choices',
	301: 'Moved Permanently',
	302: 'Found',
	303: 'See Other',
	304: 'Not Modified',
	305: 'Use Proxy',
	306: 'Switch Proxy',
	307: 'Temporary Redirect',
	308: 'Permanent Redirect',

	#4xx Client Error
	400: 'Bad Request',
	401: 'Unauthorized',
	402: 'Payment Required',
	403: 'Forbidden',
	404: 'Not Found',
	405: 'Method Not Allowed',
	406: 'Not Acceptable',
	407: 'Proxy Authentication Required',
	408: 'Request Timeout',
	409: 'Conflict',
	410: 'Gone',
	411: 'Length Required',
	412: 'Precondition Failed',
	413: 'Request Entity Too Large',
	414: 'Request-URI Too Long',
	415: 'Unsupported Media Type',
	416: 'Requested Range Not Satisfiable',
	417: 'Expectation Failed',
	418: 'I\'m a teapot',
	419: 'Authentication Timeout',
	422: 'Unprocessable Entity',
	423: 'Locked',
	424: 'Failed Dependency',
	425: 'Unordered Collection',
	426: 'Upgrade Required',
	428: 'Precondition Required',
	429: 'Too Many Requests',
	431: 'Request Header Fields Too Large',
	451: 'Unavailable For Legal Reasons',

	#5xx Server Error
	500: 'Internal Server Error',
	501: 'Not Implemented',
	502: 'Bad Gateway',
	503: 'Service Unavailable ',
	504: 'Gateway Timeout',
	505: 'HTTP Version Not Supported',
	506: 'Variant Also Negotiates',
	507: 'Insufficient Storage',
	508: 'Loop Detected',
	510: 'Not Extended',
	511: 'Network Authentication Required',
}

#The HTTPServer object
httpd = None

#For atomic handling of some resources
atoms = []

class HTTPError(Exception):
	def __init__(self, error, message=None):
		self.error = error
		self.message = message

class HTTPHandler(object):
	nonatomic = [ 'options', 'head', 'get' ]

	def __init__(self, request, response, groups):
		self.request = request
		self.response = response
		self.method = 'do_' + self.request.method.lower()
		self.groups = groups

	def respond(self):
		#HTTP Status 405
		if not hasattr(self, self.method):
			raise HTTPError(405)

		#Run the do_* method of the implementation
		return getattr(self, self.method)()

	def do_options(self):
		#Lots of magic for finding all attributes beginning with 'do_', removing the 'do_' and making it upper case, and joining the list with commas
		self.response.headers.set('Allow', ','.join([option[3:].upper() for option in dir(self) if option.startswith('do_')]))
		return 200, ''

	def do_head(self):
		#Try self again with do_get
		self.method = 'do_get'
		status, response = self.respond()
		self.response.headers.set('Content-Length', len(response))
		return status, ''

class HTTPHeaders(object):
	def __init__(self):
		self.headers = {}

	def __iter__(self):
		for key in self.headers.keys():
			yield self.retrieve(key)
		yield '\r\n'

	def __len__(self):
		return len(self.headers)

	def add(self, header):
		key, value = (item.strip() for item in header.rstrip('\r\n').split(':', 1))
		self.set(key, value)

	def get(self, key):
		return self.headers[key.lower()]

	def set(self, key, value):
		self.headers[key.lower()] = str(value)

	def unset(self, key):
		del self.headers[key.lower()]

	def retrieve(self, key):
		return key.lower().title() + ': ' + self.get(key) + '\r\n'

class HTTPErrorHandler(HTTPHandler):
	def __init__(self, request, response, groups, error=None, message=None):
		if error == None:
			self.error = 500
		else:
			self.error = error
		self.message = message

	def respond(self):
		if self.message:
			return self.error, status_messages[self.error], self.message
		else:
			return self.error, status_messages[self.error], str(self.error) + ' - ' + status_messages[self.error]

class HTTPLog(object):
	def __init__(self, log_file):
		os.makedirs(os.path.dirname(loa_file), exist_ok=True)
		self.log_file = open(log_file, 'a', 1)
		pass

	def write(self, host, message, rfc931='-', authuser='-'):
		self.log_file.write(message)

	def request(self, host, request, code='-', size='-', rfc931='-', authuser='-'):
		self.write(host, rfc931, authuser, request + ' ' + code + ' ' + size)

	def info(self, host, message, rfc931='-', authuser='-'):
		self.write(host, rfc931, authuser, 'INFO: ' + message)

	def warn(self, host, message, rfc931='-', authuser='-'):
		self.write(host, rfc931, authuser, 'WARN: ' + message)

	def error(self, host, message, rfc931='-', authuser='-'):
		self.write(host, rfc931, authuser, 'ERROR: ' + message)

class HTTPResponse(object):
	def __init__(self, request):
		self.request = request
		self.wfile = request.wfile
		self.headers = HTTPHeaders()

	def handle(self):
		try:
			if not self.request.method.lower() in self.request.handler.nonatomic:
				atomic = True
			else:
				atomic = False

			#Atomic handling of resources - wait for resource to become available if necessary
			if atomic:
				while self.request.resource in atoms:
					time.sleep(0.01)

			#Do appropriate resource locks and try to get HTTP status, response text, and possibly status message
			try:
				if atomic:
					atoms.append(self.request.resource)

				response = self.request.handler.respond()

				if atomic:
					atoms.remove(self.request.resource)
			except HTTPError as e:
				response = HTTPErrorHandler(None, None, None, e.error, e.message).respond()

			#Get data from response
			try:
				status, status_msg, response = response
			except ValueError:
				status, response = response
				status_msg = status_messages[status]

			#Convert response to bytes if necessary
			if not isinstance(response, bytes):
				response = response.encode(default_encoding)

			#Set a few necessary headers (that the handler should not change)
			self.headers.set('Server', server_version)
			self.headers.set('Date', time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.gmtime()))

			#If length is 0, the response is likely not one that needs a Content-Length or it has already been filled by a HEAD command
			length = len(response)
			if length > 0:
				self.headers.set('Content-Length', length)
		except:
			#Catch the most general errors and tell the client with the least likelihood of throwing another exception (if it still does, the streams are probably closed and there is no recovery from that except in socketserver.StreamRequestHandler)
			status, status_msg, response = HTTPErrorHandler(None, None, None, 500).respond()
			if not isinstance(response, bytes):
				response = response.encode(default_encoding)
			raise
		finally:
			#Send HTTP response
			self.wfile.write((http_version + ' ' + str(status) + ' ' + status_msg + '\r\n').encode(http_encoding))

			#Have headers written
			for header in self.headers:
				self.wfile.write(header.encode(http_encoding))

			#Write response
			self.wfile.write(response)

class HTTPRequest(socketserver.StreamRequestHandler):
	def handle(self):
		#Prepare a response in case the worst happens
		response = HTTPResponse(self)
		try:
			#Get request line
			request = str(self.rfile.readline(max_request_size), http_encoding)

			#HTTP Status 414
			#If line does not end in \r\n, it must be longer than the buffer
			if request[-2:] != '\r\n':
				raise HTTPError(414)

			#Now that we've checked it, get rid of newline
			self.request_line = request.rstrip('\r\n')

			#Try the request line and error out if can't parse it
			try:
				self.method, self.resource, self.request_http = self.request_line.split()
			#HTTP Status 400
			except ValueError:
				raise HTTPError(400)

			#HTTP Status 505
			if self.request_http != http_version:
				raise HTTPError(505)

			#Read and parse request headers
			self.headers = HTTPHeaders()
			while True:
				line = str(self.rfile.readline(max_line_size), http_encoding)

				#HTTP Status 431
				#If line does not end in \r\n, it must be longer than the buffer
				if line[-2:] != '\r\n':
					raise HTTPError(431)

				#Hit end of headers
				if line == '\r\n':
					break

				#HTTP Status 431
				if len(self.headers) >= max_headers:
					raise HTTPError(431)

				self.headers.add(line)

			#Find a matching regex to handle the request with
			self.handler = None
			for regex, handler in self.routes.items():
				match = regex.match(self.resource)
				if match:
					self.handler = handler(self, response,  match.groups())

			#HTTP Status 404
			if self.handler == None:
				raise HTTPError(404)
		except HTTPError as e:
			self.handler = HTTPErrorHandler(None, None, None, e.error, e.message)
		except:
			self.handler = HTTPErrorHandler(None, None, None, 500)
			raise
		finally:
			#We finished listening and handling early errors and so let a response class now finish up the job of talking
			response.handle()

class HTTPServer(socketserver.ThreadingTCPServer):
	def server_bind(self):
		socketserver.TCPServer.server_bind(self)
		host, port = self.socket.getsockname()[:2]
		self.server_name = socket.getfqdn(host)
		self.server_port = port

def init(address, routes, log=HTTPLog, keyfile=None, certfile=None):
	global httpd

	#Compile the regex routes and add them
	HTTPRequest.routes = {}
	for regex, handler in routes.items():
		HTTPRequest.routes[re.compile('^' + regex + '$')] = handler

	HTTPRequest.log = log

	httpd = HTTPServer(address, HTTPRequest)

	#Add SSL if specified
	if keyfile and certfile:
		httpd.socket = ssl.wrap_socket(httpd.socket, keyfile, certfile, server_side=True)

def destroy():
	global httpd

	httpd.server_close()

	httpd = None

def start():
	global httpd

	threading.Thread(target=httpd.serve_forever).start()

def stop():
	global httpd

	httpd.shutdown()
