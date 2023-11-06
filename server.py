import http.server
import socketserver
import json
from urllib.parse import parse_qs
from torbot.modules.api import get_node

PORT = 8000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        url = data['path'][0]
        node_data = get_node(url, 1)
        print(node_data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(node_data).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with open('data.json', 'rb') as file:
            self.wfile.write(file.read())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
