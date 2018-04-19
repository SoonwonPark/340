import socket
import sys


# Present status
# - can do basic GET request
# - e.g. python Client.py http://stevetarzia.com/index

# To do
# - handling errors like 301, 302 and >=400
# - chain of mutiple redirect
# - dealing with port number, now using 80
# - Check the response's content-type header.
#   Print the body to stdout only if the content-type begins with "text/html".
#   Otherwise, exit with a non-zero exit code.
# - Return an error code if the input url does not start with "http://"
# - You should not require a slash at the end of top-level urls.




# making an argument for URL based on user's typing
# e.g. python Client.py http://northwestern.edu/somepage.html in Piazza
for url in sys.argv[1:]:
    url = url

# print url for test
print("user input: " + url)


class Client:
    # constructor
    def __init__(self, urlinput):
        self.address = urlinput
        self.host = ""
        self.hostip = ""
        self.path = ""

    # set address, host, hostip, and path
    def set_ahhp(self):
        if self.address.startswith("http://"):
            third_slash = self.address.find('/', 7)
            self.path = self.address[third_slash:]
            self.address = self.address[7:third_slash]
            # self.host = socket.getfqdn(self.address)
            # self.hostip = socket.gethostbyname(self.host)
            self.hostip = "127.0.0.1"

        if self.address.startswith("https://"):
            exit("error: use 'http://'")





# construct a Client class with url
myClient = Client(url)
myClient.set_ahhp()


# print url for test
print("host: " + myClient.host)
print("host IP: " + myClient.hostip)
print("path: " + myClient.path)

# make a socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the server with port 80
mysocket.connect((myClient.hostip, 10000))

print("Trying to connect!")

# making a request on HTTP format
request = "GET "+ myClient.path + " HTTP/1.1\r\nHost: " + myClient.host+"\r\n\r\n"
print(request)

# send request to server
mysocket.send(request)

# print response from the server
print mysocket.recv(4096)