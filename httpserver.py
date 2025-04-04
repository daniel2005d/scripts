## https://gist.github.com/UniIsland/3346170
import http.server
import socketserver
import os
from http import HTTPStatus
import urllib.parse
import signal
import sys
import argparse

# Class to handle custom POST requests
class PostHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("GET")
        super().do_GET()

    def do_POST(self):
        print("<- Calling POST")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        if body:
            file_data = urllib.parse.parse_qs(body.decode())
            for item in file_data.items():
                print(item)
        # # Read POST request data
        # post_data = self.rfile.read(content_length)
        # # Parse POST data to get file data
        # try:
        #     post_params = urllib.parse.parse_qs(post_data.decode())
        #     file_data = self.rfile.read(int(post_params['Content-Length'][0]))
        # except Exception as e:
        #     self.send_response(HTTPStatus.BAD_REQUEST)
        #     self.end_headers()
        #     self.wfile.write("Error parsing POST data: {}".format(e).encode())
        #     return

        # if not file_data:
        #     self.send_response(HTTPStatus.BAD_REQUEST)
        #     self.end_headers()
        #     self.wfile.write("No file data provided in the POST request".encode())
        #     return

        # # Save the file on the server
        # file_name = "uploaded_file.txt"
        # with open(file_name, 'wb') as file:
        #     file.write(file_data.encode())

        # Respond with a confirmation
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write("File saved successfully".encode())

def signal_handler(sig, frame):
    print("Stopping Server...")
    httpd.server_close()
    #httpd.shutdown()  # Cierra el servidor HTTP
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    # Configure the server


    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5051, type=int)
    args = parser.parse_args()

    Handler = PostHandler

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print("Server on port", args.port)
        httpd.serve_forever()
