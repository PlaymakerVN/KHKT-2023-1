

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server started at http://localhost:{}/".format(PORT))
    httpd.serve_forever()



# import http.server
# import urllib.parse

# class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = '/index.html'
#         try:
#             file_to_open = open(self.path[1:]).read()
#             self.send_response(200)
#         except:
#             file_to_open = "File not found"
#             self.send_response(404)
#         self.end_headers()
#         self.wfile.write(bytes(file_to_open, 'utf-8'))

#     def do_POST(self):
#         content_length = int(self.headers.get('Content-Length', 0))
#         post_data = self.rfile.read(content_length).decode('utf-8')
        
#         # Handle the POST request here
#         # You can access the post data in the 'post_data' variable
        
#         self.send_response(200)
#         self.send_header('Content-type', 'text/plain')
#         self.end_headers()
#         self.wfile.write(b'POST request received.')
#         print(post_data)

# while True :
#     server_address = ('', 8000)
#     httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
#     httpd.serve_forever()


# import http.server
# import socket
# import urllib.parse

# # Create a socket object
# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Define the port for communication
# port = 80

# # Bind the socket to the specified port
# serversocket.bind(('localhost', port))

# # Listen for incoming connections
# serversocket.listen(1)

# print('Server listening on port', port)

# # Accept the incoming connection
# clientsocket, addr = serversocket.accept()
# print('Connected by', addr)

# # Receive the request data sent by the client
# request_data = clientsocket.recv(1024).decode('utf-8')

# # Extract the requested file path from the request
# requested_file = request_data.split()[1][1:]

# # Check if the requested file is index.html
# if requested_file == 'index.html':
#     # Read the contents of index.html
#     with open(requested_file, 'r') as file:
#         html_content = file.read()

#     # Send the HTTP response with the contents of index.html
#     response = 'HTTP/1.1 200 OK\n\n' + html_content
#     clientsocket.sendall(response.encode('utf-8'))
# else:
#     # Send a 404 Not Found response for other files
#     response = 'HTTP/1.1 404 Not Found\n\n'
#     clientsocket.sendall(response.encode('utf-8'))

# # Receive the data sent by the client
# data = clientsocket.recv(1024).decode('utf-8')

# HOST = 'localhost'
# PORT = 8000

# with MyServer((HOST, PORT), MyRequestHandler) as server:
#     print(f"Server started on {HOST}:{PORT}")
#     server.serve_forever()
# # Parse the form data
# parsed_data = urllib.parse.parse_qs(data)

# # Access the 'text' value from the parsed data
# # text = parsed_data['text'][0]

# # print('Received text:', text)

# # Close the connection
# clientsocket.close()



# import http.server
# import urllib.parse

# class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/index.html':
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             with open('index.html', 'rb') as file:
#                 self.wfile.write(file.read())
#         else:
#             super().do_GET()

#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length).decode('utf-8')
#         parsed_data = urllib.parse.parse_qs(post_data)
        
#         # Handle the POST request data
#         # You can access the data using parsed_data dictionary
#         print("POST data:", parsed_data)
        
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(b'POST request received')

# class MyServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     allow_reuse_address = True

# HOST = 'localhost'
# PORT = 8000

# with MyServer((HOST, PORT), MyRequestHandler) as server:
#     print(f"Server started on {HOST}:{PORT}")
#     server.serve_forever()