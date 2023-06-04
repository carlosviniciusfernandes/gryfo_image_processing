from http.server import BaseHTTPRequestHandler

from .router import router


class RequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, OPTIONS')
        self.end_headers()

    def do_POST(self):
        if not router.get('POST', {}).get(self.path):
            self.send_response(404)
            self.set_headers()
            return

        try:
            router['POST'][self.path](self)
        except Exception as e:
            self.send_response(500)
            self.set_headers()

    def set_headers(self, type='application/json') -> None:
        self.send_header('Content-type', type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
