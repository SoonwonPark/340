__author__ = "Byungjin Jun"

# USAGE: sudo python udp_dns_proxy.py
# sudo permission is necessary since it binds with port 53
# to test
# 1. run this locally
# 2. runt nslookup "TARGET DOMAIN" 127.0.0.1

import socket


# basic UDP DNS server in python
class DNSserver():
	def __init__(self):
		self.PORT = 53
		self.upstream_ip = "8.8.8.8"
		self.PACKET_SIZE = 1024
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.setblocking(1)

	# create a socket connection
	def start(self):
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.bind(("", self.PORT))
			print "UDP DNS Server started with port: " + str(self.PORT)
		except socket.error as e:
			print e
			self.s.shutdown(socket.SHUT_RDWR)

		while True:
			req, addr = self.s.recvfrom(self.PACKET_SIZE)
			print "DNS msg received"

			res = self.serve_dns(req)

			self.s.sendto(res, addr)

	# serve to the dns request
	def serve_dns(self, req):
		req_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		req_sock.sendto(req, (self.upstream_ip, 53))
		res = req_sock.recv(self.PACKET_SIZE)

		return res


def main():
	server = DNSserver()
	server.start()


if __name__ == '__main__':
	main()
