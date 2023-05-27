DEFAULT_PORT = 8000
DEFAULT_HOST = '127.0.0.1'

from http.server import HTTPServer
from argparse import _ArgumentGroup

from api.handler import RequestHandler


def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('serve')


def run(*args, **kwargs):
    ADDRESS = DEFAULT_HOST
    PORT = DEFAULT_PORT

    with HTTPServer((ADDRESS, PORT), RequestHandler) as server:
        try:
            print(f'Starting http server at http://{ADDRESS}:{PORT}/...')
            print(f'Quit with Ctrl+C')
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
            print('\ngood bye!')
