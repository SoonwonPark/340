__author__ = "Byungjin Jun"

# USAGE: python http_server2.py 10000
# TO TEST multi connection
# 1. run this server first
# 2. connect to this client by running: telnet localhost 10000
# 3. send a request to the server from other client (Client.py or browser)
# 4. compare to the result from http_server1.py

import select
import Queue
import socket
import sys
import os.path


# basic http server in python
# ref 1: https://docs.python.org/2/library/socket.html
# ref 2: https://pymotw.com/2/select/
class HTTPserver():
	def __init__(self, port=50000):
		self.port = port
		self.www_path = "./www"
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setblocking(0)

	# create a socket connection
	def start(self):
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind(("", self.port))
			print "Server started with port: " + str(self.port)
		except socket.error as e:
			print e
			self.s.shutdown(socket.SHUT_RDWR)

		self.s.listen(5)

		inputs = [self.s]
		outputs = []
		message_queues = {}

		# The loop for supporting multi connection with 'select'
		while inputs:
			readable, writable, exceptional = select.select(inputs, outputs, inputs)
			for r in readable:
				# accept connection
				if r is self.s:
					conn, addr = r.accept()
					print "A client connected: " + str(addr)
					conn.setblocking(0)
					inputs.append(conn)
					message_queues[conn] = Queue.Queue()
				# receive data and handle HTTP request in it
				else:
					req = r.recv(1024)
					if req:
						# process HTTP here
						res = self.serve_http(req)
						message_queues[r].put(res)
						if r not in outputs:
							outputs.append(r)
					else:
						if r in outputs:
							outputs.remove(r)
						inputs.remove(r)
						r.close()
						del message_queues[r]

			# send the response to the client
			for r in writable:
				try:
					next_msg = message_queues[r].get_nowait()
				except Queue.Empty:
					outputs.remove(r)
				else:
					r.send(next_msg)

			# if there was error, close the connection
			for r in exceptional:
				inputs.remove(r)
				if r in outputs:
					outputs.remove(r)
				r.close()
				del message_queues[r]

	# serve to the http request
	def serve_http(self, req):
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
		else:
			res = self.HTTP_response_builder(403)
			print "ERROR: no support for other methods than 'GET'"

		return res

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
	if len(sys.argv) < 2:
		print "ERROR: port number required" \
		      "USAGE: python http_server2.py 10000"
	else:
		port = int(sys.argv[1])
		if is_valid_port(port):
			server = HTTPserver(port)
			server.start()
		else:
			print "ERROR: port number must be an integer in between 1024 and 65535"


if __name__ == '__main__':
	main()
