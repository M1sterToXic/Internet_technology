from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tickets' or self.path == '/api/tickets':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'service': 'tickets-svc-s01',
                'resource': 'tickets',
                'data': ['ticket1', 'ticket2']
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/tickets' or self.path == '/api/tickets':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'service': 'tickets-svc-s01',
                'created': True,
                'data': json.loads(post_data)
            }
            self.wfile.write(json.dumps(response).encode())


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8111), Handler)
    print('Tickets service running on port 8111...')
    print('Available endpoints: /tickets, /api/tickets')
    server.serve_forever()