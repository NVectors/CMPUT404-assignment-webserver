#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        request = self.request
        #TCP protocol server
        rawDataReceived = request.recv(4096)
        dataDecoded = rawDataReceived.decode("utf-8")
        headers = dataDecoded.strip().split('\r\n')
        httpRequest = headers[0]
        method, url, protocol = httpRequest.split(" ")

        print("******\nGot a request of:\n%s\n******" % dataDecoded)

        # HTTP Request Type Response
        # HTTP GET Request only
        print("Checking HTTP Method")
        if not (self.checkHTTPRequest(request, method)):
            return

        # HTTP Request Header Response
        # Check if header format is invalid
        print("Checking HTTP Header")
        if not (self.checkHTTPHeader(request, httpRequest)):
            return

        # HTTP URL Response
        # Check the url recieved, serve only ./www/ or ./www/deeper/
        print("Checking for valid URL")
        if not (self.validURL(request, url)):
            return

        # HTTP URL Response
        # Check for HTTP 301 if / is missing at the end of ./www or ./www/deeper
        print("Checking for HTTP 301")
        url = self.redirectURL(request, url)

        print("Checking if URL is the root")
        url_to_path = self.pathURL(url)
        print(url_to_path)

        # TO DO READ FILE AND GET CONTENT HEADER INFORMATION






        # At the end if there no issues
        response = "%s 200 OK\n" % protocol
        request.sendall(bytearray(response,"utf-8"))

    def checkHTTPRequest(self, request, method):
        if not ("GET" in method):
            response = "HTTP/1.1 405 Method Not Allowed\n"
            request.sendall(bytearray(response,"utf-8"))
            return False
        return True

    def checkHTTPHeader(self, request, httpRequest):
        if (len(httpRequest.split(" ")) != 3):
           response = "HTTP/1.1 400 Bad Request\n"
           request.sendall(bytearray(response,"utf-8"))
           return False
        return True

    def validURL(self, request, url):
        local_path = "./www" + url
        if os.path.isdir(local_path) or os.path.isfile(local_path):
            return True
        else:
            response = "HTTP/1.1 404 Not Found\n"
            request.sendall(bytearray(response,"utf-8"))
            return False

    def redirectURL(self, request, url):
        if not ("/" in url[-1]):
            response = "HTTP/1.1 301 Moved Permanently\n"
            request.sendall(bytearray(response,"utf-8"))
            return url + '/'
        return url

    def pathURL(self, url):
        local_path = "./www" + url
        if os.path.isfile(local_path):
            return local_path
        else:
            # Has to be a directory if it not a file
            assert(os.path.isdir(local_path))
            dirURL = os.path.join(local_path, 'index.html')
            return dirURL


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
