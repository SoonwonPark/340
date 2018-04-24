import socket
import sys
import re

# << Project Requirement>
#
# Use HTTP "GET" method : complete
#
# Include "Host:///" header : complete
#
# 301, 302 Rdeirection : complete
#  - example: python Client.py http://airbedandbreakfast.com/
#  - example: python Client.py http://maps.google.com/
#
# Handle a chain of multiple redirect :complete(10 redirection) : complete
#  - example: Python Client.py http://thefacebook.com/
#
# Return unix exit code 0 on success, non-zero on failure : complete
#
# If you visit a https page, return an exit with error : complete
#
# Return an error code if the input url does not start with "http://" : complete
#
# Allow request urls to include a port number. : complete
#  - example: python Client.py http://portquiz.net:8080/
#
# Do not requre a slash at the end of top-level urls : complete
#  - example: python Client.py http://stevetarzia.com
#  - example: python Client.py http://stevetarzia.com/
#
# You should be able to handle large pages : complete
#  - example: python Client.py http://stevetarzia.com/libc.html
#


url = sys.argv[1]


# print url for test
print("user input: " + url)


class Client:

    def __init__(self, urlinput):
        self.address = urlinput
        self.host = ""
        self.hostip = ""
        self.path = ""
        self.request = ""
        self.mysocket = None
        self.PACKET_SIZE = 4096
        self.recvmessage = ""
        self.status_code = ""
        self.port = ""
        self.newaddress = ""
        self.contenttype = ""
        self.contentlength = ""


    def __del__(self):
        print("")


    def setaddress(self, newadd):
        self.address = newadd


    def makesocket(self):
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def deletesocket(self):
        self.mysocket = None

    # set address, host, hostip, and path
    def set_ahhp(self):
        if self.address.startswith("http://"):

            third_slash = self.address.find('/', 7)
            if third_slash == -1:
                self.address = self.address + "/"
                third_slash = len(self.address)-1
            else :
                third_slash = third_slash

            self.path = self.address[third_slash:]
            self.address = self.address[7:third_slash]

            portlocation = self.address.find(':', 7)
            if portlocation == -1:
                self.address = self.address
                self.port = 80
            else:
                self.port = int(self.address[portlocation+1:])
                self.address = self.address[:portlocation]
                # print("address2: " + self.address)

            print("address: " + self.address)
            print("path: " + self.path)
            if self.address == "localhost" :
                self.host = "localhost"
            else:
                self.host = socket.getfqdn(self.address)
            print("host: " + self.host)
            if self.address == "localhost":
                self.hostip = "127.0.0.1"
            else:
                self.hostip = socket.gethostbyname(self.host)
            print("hostip: " + self.hostip)
            self.request = "GET " + self.path + " HTTP/1.1\r\nHost: " + self.host + "\r\n\r\n"
            self.request = "GET " + self.path + " HTTP/1.1\r\nHost: " + self.address + "\r\n\r\n"
            print("port: " + str(self.port))


        elif self.address.startswith("https://"):
            exit("error: you input 'https://',  please use 'http://'")

        else :
            exit("Error, please use 'http://'")

    def connect(self):
        print("Trying to Connect")
        print("hostip: "+ self.hostip)
        self.mysocket.connect((self.hostip, self.port))
        print("port: " + str(self.port))

    def sendrequest(self):
        print(self.request)
        self.mysocket.send(self.request)

    def receive(self):
        self.recvmessage = self.mysocket.recv(self.PACKET_SIZE)
        data = self.recvmessage.split('\r\n\r\n')
        header = data[0]
        content = data[1]
        splitted_header = re.split(' |\n', header)
        self.status_code = splitted_header[1]

        if self.status_code == "200":
            print("Status Code: " + str(self.status_code))
            self.contenttype = splitted_header[splitted_header.index("Content-Type:") + 1]
            print("content-type: " + self.contenttype)
            self.contentlength = splitted_header[splitted_header.index("Content-Length:") + 1]

            if self.contenttype == "text/html":
                length_left = int(self.contentlength) - self.PACKET_SIZE
                while length_left > 0:
                    print length_left
                    chunk = self.mysocket.recv(self.PACKET_SIZE)
                    content += chunk
                    length_left -= self.PACKET_SIZE
                    print length_left
                print(self.recvmessage)
                print "end"

            else:
                sys.exit("content-type is not text/html")


        elif self.status_code == "301" or self.status_code == "302" :
            print("status code: " + str(self.status_code))

        elif self.status_code >= "400" :
            print("Status code: " + str(self.status_code))


    def stoporfoward(self):

        if self.status_code == "301" or self.status_code == "302" :
            Location_start = self.recvmessage.find("Location") + 8
            Location_end = self.recvmessage.find("\r", Location_start)
            print("Redirected to: " + self.recvmessage[Location_start+2:Location_end])
            self.newaddress = self.recvmessage[Location_start+2:Location_end]
            self.mysocket.close()
            return self.newaddress

        elif self.status_code == "200":
            self.newaddress = ""
            # self.mysocket.close()
            print"\n"
            print("Fetch Success")
            sys.exit(0)

        elif self.status_code >= "400":
            self.newaddress = ""
            # self.mysocket.close()
            sys.exit("Error, Status Code is 400 or 400+")





def main():

    myClient = Client(url)
    myClient.makesocket()
    myClient.set_ahhp()
    myClient.connect()
    myClient.sendrequest()
    myClient.receive()
    result = myClient.stoporfoward()

    count = 9

    while(count > 0) :

        if result != myClient.address:
            myClient = Client(result)
            myClient.makesocket()
            myClient.set_ahhp()
            myClient.connect()
            myClient.sendrequest()
            myClient.receive()
            result = myClient.stoporfoward()
            myClient.__del__()
            count = count -1

    print("redirection is over 10")



# run main function
main()