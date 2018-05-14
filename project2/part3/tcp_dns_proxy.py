__author__ = "Byungjin Jun"

# USAGE: sudo python tcp_dns_proxy.py
# sudo permission is necessary since it binds with port 53
# to test,
# 1. run this locally
# 2. run nslookup "TARGET DOMAIN(tcp)" 127.0.0.1
# example: nslookup -type=TXT long.stevetarzia.com 127.0.0.1
#          nslookup "-set vc" yahoo.com 127.0.0.1

import socket
import sys
import select
import Queue


# basic TCP DNS server in python
class DNSProxy():
	def __init__(self):
		self.PORT = 53
		self.upstream_ip = "8.8.8.8"
		self.PACKET_SIZE = 1024
		# AF_INET: an address family (IPv4) that the socket uses
		# SOCK_STREAM: TCP socket / SOCK_DGRAM: UDP socket
		self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp_sock.setblocking(1)
		self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp_sock.setblocking(1)

	# create a socket connection
	def start(self):
		# start listening to UDP connections
		e = self.listen_UDP()
		if e:
			print e
			sys.exit(1)
		# start listening to TCP connections
		e = self.listen_TCP()
		if e:
			print e
			sys.exit(1)

		inputs = [self.udp_sock, self.tcp_sock]
		outputs = []
		message_queues = {}

		while inputs:
			readable, writable, exceptional = select.select(inputs, outputs, inputs)
			for r in readable:
				# accept TCP connection
				if r is self.tcp_sock:
					conn, addr = r.accept()
					print "DNS msg received (TCP)"
					conn.setblocking(1)
					inputs.append(conn)
					message_queues[conn] = Queue.Queue()
				# accept and serve UDP connection
				elif r is self.udp_sock:
					req, addr = self.udp_sock.recvfrom(self.PACKET_SIZE)
					print "DNS msg received (UDP)"
					if req:
						res = self.serve_dns_udp(req)
						self.udp_sock.sendto(res, addr)
						print "DNS response sent to the client"

				# receive data and handle DNS request (TCP) in it
				else:
					req = r.recv(self.PACKET_SIZE)
					if req:
						# process DNS here
						res = self.serve_dns_tcp(req)
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
					print "DNS response sent to the client (TCP)"

			# if there was error, close the connection
			for r in exceptional:
				inputs.remove(r)
				if r in outputs:
					outputs.remove(r)
				r.close()
				del message_queues[r]

	def listen_UDP(self):
		try:
			self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.udp_sock.bind(("", self.PORT))
			print "DNS Server started with port: " + str(self.PORT)
			return None
		except socket.error as e:
			self.udp_sock.shutdown(socket.SHUT_RDWR)
			return e

	def listen_TCP(self):
		try:
			self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.tcp_sock.bind(("", self.PORT))
			print "TCP Server started with port: " + str(self.PORT)
			self.tcp_sock.listen(5)
			return None
		except socket.error as e:
			self.tcp_sock.shutdown(socket.SHUT_RDWR)
			return e

	# serve to the dns request (udp)
	def serve_dns_udp(self, req):
		req_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		req_sock.sendto(req, (self.upstream_ip, 53))
		req_sock.settimeout(1.0)
		try:
			res = req_sock.recv(self.PACKET_SIZE)
		except socket.timeout:
			res = self.serve_dns_udp(req)
		return res

	# serve to the dns request (tcp)
	def serve_dns_tcp(self, req):
		req_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		req_sock.connect((self.upstream_ip, 53))
		req_sock.sendto(req, (self.upstream_ip, 53))
		res = ""

		# receive tcp dns respnse
		while True:
			chunk = req_sock.recv(self.PACKET_SIZE)
			if len(chunk) == 0:
				break
			else:
				res = res + chunk

		return res


def main():
	server = DNSProxy()
	server.start()


if __name__ == '__main__':
	main()
