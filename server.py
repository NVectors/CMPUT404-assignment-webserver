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
        rawDataReceived = request.recv(4096)            # TCP protocol server
        dataDecoded = rawDataReceived.decode("utf-8")   # Convert bytes to string
        headers = dataDecoded.strip().split('\r\n')     # Split up HTTP Request headers
        start_line = headers[0]                         # Start-line header

        print("Got a request of:\n%s\n" % dataDecoded)

        # HTTP Request Response
        # Check if header format is invalid
        print("Checking HTTP Header")
        if not (self.checkHTTPRequest(request, start_line)):
            return

        method, request_target, version = start_line.split(" ")
        local_path = "./www" + request_target

        if os.path.isdir(local_path):
            print(local_path[-1])
            if local_path[-1] == "/":
                local_path += "index.html"
                response = self.checkFileExt(local_path)
                print(response)
                request.sendall(bytearray(response,"utf-8"))
            elif local_path[-1] != "/":
                base_url = "http://127.0.0.1:8080/www"
                response = "HTTP/1.1 301 Moved Permanently Location: " + base_url + request_target + "/" + "\r\n\r\n"
                request.sendall(bytearray(response,"utf-8"))

        elif os.path.isfile(local_path):
            # Read file and get content
            print("Checking file ext.")
            response = self.checkFileExt(local_path)
            request.sendall(bytearray(response,"utf-8"))



    def checkHTTPRequest(self, request, start_line):
        # Start-line must contain: HTTP Method, Request Target, HTTP Version
        if (len(start_line.split()) != 3):
            response = "HTTP/1.1 400 Bad Request\r\n"
            request.sendall(bytearray(response,"utf-8"))
            return False
        # No POST/PUT/DELETE
        methodHTTP = start_line.split()[0]
        if not ("GET" in methodHTTP):
            response = "HTTP/1.1 405 Method Not Allowed\r\n"
            request.sendall(bytearray(response,"utf-8"))
            return False
        # Only HTTP Version 1.1
        versionHTTP = start_line.split()[2]
        if not ("HTTP/1.1" in versionHTTP):
            response = "HTTP/1.1 400 Bad Request\r\n"
            request.sendall(bytearray(response,"utf-8"))
            return False
        return True

    def checkFileExt(self,url):
        file = open(url, "r")
        content = file.read().replace("\n", "")

        # Serve only HTML and CSS
        filename, file_extension = os.path.splitext(url)
        if file_extension == ".html":
            MIME_type = "text/html"
        elif file_extension == ".css":
            MIME_type = "text/css"
        else:
            response =  "HTTP/1.1 404 Not Found\n"

        response = "HTTP/1.1 200 OK\r\nContent-Type:" + MIME_type + "\r\n\r\n" + content +"\r\n"
        file.close()
        return response


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
