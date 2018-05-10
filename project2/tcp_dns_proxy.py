__author__ = "Byungjin Jun"

# USAGE: sudo python udp_dns_proxy.py
# sudo permission is necessary since it binds with port 53
# to test
# 1. run this locally
# 2. runt nslookup "TARGET DOMAIN(tcp)" 127.0.0.1
# 3. example: nslookup -type=TXT long.stevetarzia.com 127.0.0.1
#             nslookup "-set vc" yahoo.com 127.0.0.1

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
        self.t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t.setblocking(1)

    # create a socket connection
    def start(self):
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(("", self.PORT))
            self.t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.t.bind(("", self.PORT))
            print "DNS Server started with port: " + str(self.PORT)
        except socket.error as e:
            print e
            self.s.shutdown(socket.SHUT_RDWR)

        while True:
            req, addr = self.s.recvfrom(self.PACKET_SIZE)
            print "DNS msg received"

            res = self.serve_dns(req)
            resbytearr = bytearray(res) 

            # when response is truncated
            if resbytearr[2] & 2 == 2:
                # send truncated udp response to the clinet
                self.s.sendto(res, addr)
                # accept connection
                self.t.listen(5)
                conn_tcp, addr_tcp = self.t.accept()
                # receive tcp dns request
                req_tcp, addr_recv_tcp = conn_tcp.recvfrom(self.PACKET_SIZE)
                # receive tcp dns resonse from 8.8.8.8
                res_tcp = self.serve_dns_tcp(req_tcp)
                # send tcp dsn response to the client
                conn_tcp.sendto(res_tcp, addr_tcp)

            # when response is not truncated
            else: 
                self.s.sendto(res, addr)

    # serve to the dns request(udp)
    def serve_dns(self, req):
        req_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        req_sock.sendto(req, (self.upstream_ip, 53))
        res = req_sock.recv(self.PACKET_SIZE)

        return res

    # serve to the dns request(tcp)
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
    server = DNSserver()
    server.start()


if __name__ == '__main__':
    main()
