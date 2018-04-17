import socket
import sys

# making parameter based on user
# e.g. python Client.py http://northwestern.edu/somepage.html in Piazza
for userinput in sys.argv[1:]:
    userinput = userinput

# # address test
print("user input: " + userinput)


def extract_address(input):
    if input.startswith("http://"):
        third_slash = input.find('/', 7)
        address = input[7:third_slash]
        print("address: " + address)
        return address
    if input.startswith("https://"):
        exit("error: use 'http://'")

def extract_path(input):
    third_slash = input.find('/', 7)
    path = input[third_slash:]
    print("path: " + path)
    return path


address = extract_address(userinput)
path = extract_path(userinput)


# make a socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.getfqdn(address)
hostip = socket.gethostbyname(host)
print("host: " + host)
print("host IP: " + hostip)

# # host and port should be decided
# # now localhost
# # host = mysocket.set
# port = 1247
#
# # connect to the server
mysocket.connect((hostip, 80))
# # mysocket.create_connection(host)
#
# print mysocket.recv(4096)
#
# # test for sending message
# inpt = raw_input('type anything and enter... ')
# mysocket.send(inpt)
#
# print "your message has been sent"