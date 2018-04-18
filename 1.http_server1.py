__author__ = "Byungjin Jun"

import sys
import socket

# Do the following repeatedly:
# a. Accept a new connection on the accept socket.
# We’ll call this new socket the "connection socket." (What is the 5-tuple describing the connection?)
#
# b. Read the HTTP request from the connection socket and parse it. (How do you know how many bytes to read?)
#
# c. Check to see if the requested file requested exists (and ends with ".htm" or ".html").
#
# d. If the file exists, construct the appropriate HTTP response (What’s the right response code?)
# write the HTTP header to the connection socket, and then open the file and write its contents to the connection socket (thus writing the HTTP body).
#
# e. If the file doesn’t exist, construct a HTTP error response (404 Not Found) and write it to the connection socket.
#
# f. Close the connection socket.


# basic http server in python
# reference: https://docs.python.org/2/library/socket.html
class HTTPserver():
	def __init__(self, port=12345):
		self.port = port
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def start(self):
		try:
			self.s.bind((socket.gethostname(), self.port))
			print "Server started with port: " + str(self.port)
		except socket.error as e:
			print "Cannot bind to port: " + str(self.port)
			self.s.close()

		# backlog arg is the maximum number of queued connections which should be at least 1
		# When the max backlog is reached, the server doesn't respond to SYN message.
		self.s.listen(5)
		conn, addr = self.s.accept()
		print "A client connected: " + addr
		# keep listen on accepted connection in the loop
		while True:
			req = conn.recv(1024)
			if not req:
				break
			else:
				self.serve_http(req, conn, addr)
			# conn.sendall(data)
		conn.close()


	def serve_http(self, req, conn, addr):
		print req


	# d
	def HTTP_response_builder(self):
		return True


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
	port = sys.argv[1]
	if is_valid_port(port):
		server = HTTPserver(port)
		server.start()
	else:
		print "port number must be an integer in between 1024 and 65535"
