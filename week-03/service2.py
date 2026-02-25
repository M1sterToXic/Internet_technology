from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/other' or self.path == '/api/other':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'service': 'other-service',
                'resource': 'other',
                'data': ['other1', 'other2']
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/other' or self.path == '/api/other':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'service': 'other-service',
                'created': True,
                'data': json.loads(post_data)
            }
            self.wfile.write(json.dumps(response).encode())


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8112), Handler)
    print('Other service running on port 8112...')
    print('Available endpoints: /other, /api/other')
    server.serve_forever()