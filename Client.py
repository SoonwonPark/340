import socket
import sys

# making an argument for URL based on user's typing
# e.g. python Client.py http://northwestern.edu/somepage.html in Piazza
for url in sys.argv[1:]:
    url = url

# print url for test
print("user input: " + url)


def extract_address(input):
    if input.startswith("http://"):
        third_slash = input.find('/', 7)
        address = input[7:third_slash]
        return address
    if input.startswith("https://"):
        exit("error: use 'http://'")

def extract_path(input):
    third_slash = input.find('/', 7)
    path = input[third_slash:]
    return path


# set hostip, path
address = extract_address(url)
host = socket.getfqdn(address)
hostip = socket.gethostbyname(host)
path = extract_path(url)

# print url for test
print("host: " + host)
print("host IP: " + hostip)
print("path: " + path)

# make a socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the server with port 80
mysocket.connect((hostip, 80))

print("connected!")

# making a request on HTTP format
request = "GET "+ path + " HTTP/1.1\r\nHost: " + host+"\r\n\r\n"
print(request)

# send request to server
mysocket.send(request)

# print response from the server
print mysocket.recv(4096)
