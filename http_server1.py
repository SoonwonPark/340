__author__ = "Byungjin Jun"

# USAGE: python http_server1.py 10000

import socket
import sys
import os.path


# basic http server in python
# reference: https://docs.python.org/2/library/socket.html
class HTTPserver():
	def __init__(self, port=50000):
		self.port = port
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.www_path = "./www"

	# create a socket connection
	def start(self):
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind((socket.gethostname(), self.port))
			print "Server started with port: " + str(self.port)
		except socket.error as e:
			print "ERROR: Cannot bind to port: " + str(self.port)
			self.s.shutdown(socket.SHUT_RDWR)

		# listen on accepted connection in the loop
		while True:
			# backlog arg is the maximum number of queued connections which should be at least 1
			# When the max backlog is reached, the server doesn't respond to SYN message.
			self.s.listen(5)
			conn, addr = self.s.accept()
			print "A client connected: " + str(addr)

			req = conn.recv(1024)
			self.serve_http(req, conn)

	# serve to the http request
	def serve_http(self, req, conn):
		req_split = req.split(' ')
		req_method = req_split[0]
		if len(req_split) > 1:
			req_file = req_split[1]
		else:
			req_file = '/'
		print "method: " + req_method
		print "requested path: " + req_file

		if req_method == "GET":
			# htm / html: 200 ok
			# not htm / html: 403 forbidden
			# no file: 404 not found
			if os.path.isfile(self.www_path + req_file):
				if req_file.split('.')[1] in ('htm', 'html'):
					res = self.HTTP_response_builder(200, self.www_path + req_file)
				else:
					res = self.HTTP_response_builder(403)
			else:
				res = self.HTTP_response_builder(404)
			conn.send(res)
		else:
			print "ERROR: no support for other methods than 'GET'"

		conn.close()

	# create a response with header and content
	def HTTP_response_builder(self, code, path=''):
		content = ''
		if code == 200:
			f = open(path, 'rb')
			content = f.read()
			f.close()

		content_len = len(content)
		header = self.generate_HTTP_header(code, content_len)
		print header

		res = header.encode() + '\r\n\r\n' + content

		return res

	# generate a simple HTTP header
	def generate_HTTP_header(self, code, content_len):
		if code == 200:
			header = 'HTTP/1.1 200 OK\n'
			header += 'Content-Length: ' + str(content_len) + '\n'
			header += 'Content-Type: text/html\n'
		elif code == 403:
			header = 'HTTP/1.1 403 Forbidden\n'
		elif code == 404:
			header = 'HTTP/1.1 404 Not Found\n'
		else:
			header = ''
			print "this is not the case yet"

		header += "Server: Python server/2.7"

		return header


# check if port is an integer and in between 1024 and 65535
def is_valid_port(port):
	if isinstance(port, int):
		if port < 1024 or port > 65535:
			return False
		else:
			return True
	else:
		return False


def main():
	port = int(sys.argv[1])
	if is_valid_port(port):
		server = HTTPserver(port)
		server.start()
	else:
		print "ERROR: port number must be an integer in between 1024 and 65535"


if __name__ == '__main__':
	main()
