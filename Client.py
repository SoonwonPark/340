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
            self.host = socket.getfqdn(self.address)
            self.hostip = socket.gethostbyname(self.host)

        if self.address.startswith("https://"):
            exit("error: use 'http://'")



class ManageSocket:

    def __init__(self, input_hostip, input_path, input_host):
        self.hostip = input_hostip
        self.minesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request = "GET "+ input_path + " HTTP/1.1\r\nHost: " + input_host+"\r\n\r\n"
        self.recvmessage = ""
        self.status_code = ""
        self.redirect = ""

    def connect(self):
        print("Trying to Connect")
        self.minesocket.connect((self.hostip, 80))

    def sendrequest(self):
        print(self.request)
        self.minesocket.send(self.request)

    def receive(self):
        self.recvmessage = self.minesocket.recv(4096)
        # print("Print Original Message")
        # print(self.recvmessage)
        # print("Print Extracted Message")
        self.status_code = self.recvmessage[9:12]
        # print("status code: " + self.status_code)

    def foward(self):
        if self.status_code == "301" or self.status_code == "302" :
            Location_start = self.recvmessage.find("Location")
            Location_end = self.recvmessage.find("\r", Location_start)
            print("redirected to: " + self.recvmessage[Location_start:Location_end])
            

        if self.status_code == "200" :
            print(self.recvmessage)
            # print("Success")






def main():

    myClient2 = Client(url)
    myClient2.set_ahhp()

    mysocket2 = ManageSocket(myClient2.hostip, myClient2.path, myClient2.host)
    mysocket2.connect()
    mysocket2.sendrequest()
    mysocket2.receive()
    mysocket2.foward()







# run main function
main()









#
# # construct a Client class with url
# myClient = Client(url)
# myClient.set_ahhp()
#
#
# # print url for test
# print("host: " + myClient.host)
# print("host IP: " + myClient.hostip)
# print("path: " + myClient.path)
#
# # make a socket
# mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # connect the server with port 80
# mysocket.connect((myClient.hostip, 80))
#
# print("Trying to connect!")
#
# # making a request on HTTP format
# request = "GET "+ myClient.path + " HTTP/1.1\r\nHost: " + myClient.host+"\r\n\r\n"
# print(request)
#
# # send request to server
# mysocket.send(request)
#
# # print response from the server
# print mysocket.recv(4096)