# このサンプルプログラムは開発・テスト用であり、本番環境では使わないこと

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from openai_sample import call_open_ai

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'error': 'Not found'
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def _send_cors_header(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self._send_cors_header()
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/openai':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                content = str(data["content"])
                print("received >> ", data)
                result = call_open_ai(content)
                print("result >> ", result)
                self.send_response(200)
                self._send_cors_header()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "result": result
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except (json.JSONDecodeError, KeyError):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'error': 'Invalid JSON'
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'error': 'Not found'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    print(f'http://localhost:8000')
    httpd.serve_forever()


if __name__ == "__main__":
    run(handler_class=CustomHandler)