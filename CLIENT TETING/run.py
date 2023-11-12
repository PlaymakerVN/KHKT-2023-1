import http.server
import urllib.parse
import handle

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print("POSTED:", post_data)
        response=handle.testing(post_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # response = "Hello, client!"
        self.wfile.write(response.encode('utf-8'))

while True :
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    httpd.serve_forever()
