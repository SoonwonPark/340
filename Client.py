import socket
import sys

# making parameter based on user
# e.g. python Client.py http://northwestern.edu/somepage.html in Piazza
for address in sys.argv[1:]:
    address += address

# address test
print address

# make a socket
mysocket = socket.socket()

# host and port should be decided
# now localhost
host = '127.0.0.1'
port = 1247

# connect to the server
mysocket.connect((host, port))

print mysocket.recv(4096)

# test for sending message
inpt = raw_input('type anything and enter... ')
mysocket.send(inpt)

print "your message has been sent"