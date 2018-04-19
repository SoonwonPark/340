__author__ = "Byungjin Jun"

import socket
import sys
import os.path


# basic http server in python
# reference: https://docs.python.org/2/library/socket.html
class HTTPserver():
	def __init__(self, port=10000):
		self.port = port
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.www_path = "./www"

	# create a socket connection
	def start(self):
		try:
			self.s.bind((socket.gethostname(), self.port))
			print "Server started with port: " + str(self.port)
		except socket.error as e:
			print "ERROR: Cannot bind to port: " + str(self.port)
			self.s.close()

		# backlog arg is the maximum number of queued connections which should be at least 1
		# When the max backlog is reached, the server doesn't respond to SYN message.
		self.s.listen(5)
		conn, addr = self.s.accept()
		print "A client connected: " + str(addr)
		# listen on accepted connection in the loop
		while True:
			req = conn.recv(1024)
			if not req:
				break
			else:
				self.serve_http(req, conn)
		conn.close()

	# serve to the http request
	def serve_http(self, req, conn):
		req_split = req.split(' ')
		req_method = req_split[0]
		req_file = req_split[1]
		print "method: " + req_method
		print "requested path: " + req_file
		if req_method == "GET":
			if os.path.isfile(self.www_path + req_file):
				res = self.HTTP_response_builder(200, self.www_path + req_file)
			else:
				res = self.HTTP_response_builder(404, self.www_path + req_file)
			conn.send(res)
		else:
			print "ERROR: no support for other methods than 'GET'"

	# create a response with header and content
	def HTTP_response_builder(self, code, path):
		res = self.generate_HTTP_header(code)
		print res
		if code == 200:
			f = open(path, 'rb')
			content = f.read()
			f.close()

			res = res.encode() + content
		else:
			"WARNING: cannot find requested file"
		return res

	# generate a simple HTTP header
	def generate_HTTP_header(self, code):
		header = 'HTTP/1.1'
		if code == 200:
			header += ' 200 OK\n'
		elif code == 404:
			header += ' 404 Not Found\n'
		else:
			"this is not the case yet"

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
