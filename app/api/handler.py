from http.server import BaseHTTPRequestHandler

from api.router import router


class RequestHandler(BaseHTTPRequestHandler):


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
        self.end_headers()
