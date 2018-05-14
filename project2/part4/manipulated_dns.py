__author__ = "Byungjin Jun"

# USAGE: sudo python tcp_dns_proxy.py
# sudo permission is necessary since it binds with port 53
# to test,
# sudo python manipulated_dns.py 18.188.183.162


import socket
import select
import Queue
import sys


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
        self.awspublic = sys.argv[1]

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
                        res = self.check_no_such_name(res, req)
                        self.udp_sock.sendto(res, addr)
                        print "DNS response sent to the client"

                # receive data and handle DNS request (TCP) in it
                else:
                    req = r.recv(self.PACKET_SIZE)
                    reqbytearr = bytearray(req)
                    if req:
                        # process DNS here
                        res = self.serve_dns_tcp(req)
                        res = self.check_no_such_name(res, req)
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

    def check_no_such_name(self, res, req):

        resbytearr = bytearray(res)

        # if the original resonse says that "no such name"
        if resbytearr[3] & 3 == 3:

            # Transaction ID extracted from original res
            Tid = res[0:2]
            # flags
            Flags = self.make_flag()
            # Counts
            Counts = self.make_counts()
            # Queries
            Queries = req[12:]
            # Answer
            Answer = self.make_answer()

            res = Tid + Flags + Counts + Queries + Answer

            return res

        else:
            return res


    def make_bit(self, data):
        return chr(int(data, 2))


    def make_flag(self):
        # flags
        QR = '1'
        OPcode = '0000'
        AA = '0'
        TC = '0'
        RD = '1'

        RA = '1'
        Z = '000'
        Rcode = '0000'

        Flags0 = QR + OPcode + AA + TC + RD
        Flags0 = self.make_bit(Flags0)
        Flags1 = RA + Z + Rcode
        Flags1 = self.make_bit(Flags1)
        Flags = Flags0 + Flags1

        return Flags

    def make_counts(self):

        QDCOUNT0 = '00000000'
        QDCOUNT0 = self.make_bit(QDCOUNT0)
        QDCOUNT1 = '00000001'
        QDCOUNT1 = self.make_bit(QDCOUNT1)

        # ANCOUNT
        ANCOUNT0 = '00000000'
        ANCOUNT0 = self.make_bit(ANCOUNT0)
        ANCOUNT1 = '00000001'
        ANCOUNT1 = self.make_bit(ANCOUNT1)

        # ARCOUNT
        ARCOUNT0 = '00000000'
        ARCOUNT0 = self.make_bit(ARCOUNT0)
        ARCOUNT1 = '00000000'
        ARCOUNT1 = self.make_bit(ARCOUNT1)

        # ADCOUNT
        ADCOUNT0 = '00000000'
        ADCOUNT0 = self.make_bit(ADCOUNT0)
        ADCOUNT1 = '00000000'
        ADCOUNT1 = self.make_bit(ADCOUNT1)

        Counts = QDCOUNT0 + QDCOUNT1 + ANCOUNT0 + ANCOUNT1 + ARCOUNT0 + ARCOUNT1 + ADCOUNT0 + ADCOUNT1

        return Counts


    def make_answer(self):

        # Name
        Name0 = '11000000'
        Name0 = self.make_bit(Name0)
        Name1 = '00001100'
        Name1 = self.make_bit(Name1)
        Name = Name0 + Name1

        # Type = A
        Type0 = '00000000'
        Type0 = self.make_bit(Type0)
        Type1 = '00000001'
        Type1 = self.make_bit(Type1)
        Type = Type0 + Type1

        # Class = IN
        Class0 = '00000000'
        Class0 = self.make_bit(Class0)
        Class1 = '00000001'
        Class1 = self.make_bit(Class1)
        Class = Class0 + Class1

        # TTL = 300
        Ttl0 = '00000000'
        Ttl0 = self.make_bit(Ttl0)
        Ttl1 = '00000000'
        Ttl1 = self.make_bit(Ttl1)
        Ttl2 = '00000001'
        Ttl2 = self.make_bit(Ttl2)
        Ttl3 = '00101100'
        Ttl3 = self.make_bit(Ttl3)
        Ttl = Ttl0 + Ttl1 + Ttl2 + Ttl3

        # Data Length, A type is 4
        Dl0 = '00000000'
        Dl0 = self.make_bit(Dl0)
        # Dl1 = '00110100'
        Dl1 = '00000100'
        Dl1 = self.make_bit(Dl1)
        Dl = Dl0 + Dl1

        # Domain Name
        Dname = self.awspublic
        Dname_splited = Dname.split(".")
        first = int(Dname_splited[0]) & 255
        first = format(first, '08b')
        first = self.make_bit(first)
        second = int(Dname_splited[1]) & 255
        second = format(second, '08b')
        second = self.make_bit(second)
        third = int(Dname_splited[2]) & 255
        third = format(third, '08b')
        third = self.make_bit(third)
        fourth = int(Dname_splited[3]) & 255
        fourth = format(fourth, '08b')
        fourth = self.make_bit(fourth)
        Dname = first + second + third + fourth

        Answer = Name + Type + Class + Ttl + Dl + Dname

        return Answer


def main():
    server = DNSProxy()
    server.start()


if __name__ == '__main__':
    main()
