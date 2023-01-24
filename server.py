#  coding: utf-8
import socketserver

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

        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages

        # HTTP Request Type Response
        # GET Request only
        self.checkHTTPRequest(request, method)

        # HTTP Request Header Response
        # Check if header format is invalid
        self.checkHTTPHeader(request, httpRequest)

        # TO DO
        # Check file path


    def checkHTTPRequest(self, request, method):
        if ("GET" in method):
            response = "HTTP/1.1 200 OK\n"
            request.sendall(bytearray(response,"utf-8"))
        else:
            response = "HTTP/1.1 405 Method Not Allowed\n"
            request.sendall(bytearray(response,"utf-8"))

    def checkHTTPHeader(self, request, httpRequest):
        if (httpRequest.split(" ") != 3):
           response = "HTTP/1.1 400 Bad Request\n"
           request.sendall(bytearray(response,"utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
