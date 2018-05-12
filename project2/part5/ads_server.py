__author__ = "Byungjin Jun"

# USAGE: python ads_server.py

import select
import Queue
import socket
import re


class AdsServer():
	def __init__(self):
		self.port = 80
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setblocking(1)

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
					conn.setblocking(1)
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
		req_split = re.split(' |\n', req)
		method = req_split[0]
		hostname = req_split[req_split.index("Host:") + 1]
		print "method: " + method
		print "hostname: " + hostname

		if method == "GET":
			res = self.HTTP_response_builder(200, hostname)
		else:
			res = self.HTTP_response_builder(403)
			print "ERROR: no support for other methods than 'GET'"

		return res

	# create a response with header and content
	def HTTP_response_builder(self, code, hostname=''):
		content = ''
		if code == 200:
			content = '''
				<html>
					<head>
						<title>340 Networking project 2</title>
					</head>
					<body>
						You are looking for {hostname}<br />
						It is probably a wrong site. You may want to visit "https://github.com/ByungjinJun" instead.
					</body>
				</html>
				'''.format(hostname=hostname)

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


def main():
	server = AdsServer()
	server.start()


if __name__ == '__main__':
	main()
