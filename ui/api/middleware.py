from typing import Callable

from .adapter import RequestAdapter
from .protocols import HTTPRequestHandler
from .exceptions import APIException


class APIMiddleware:

    @staticmethod
    def _get_formats(content_type:str ) -> tuple:
        if 'json' in content_type:
            return ('json', 'application/json')

        if 'multipart/form-data' in content_type:
            return ('bytes', 'image/png')

    def __init__(self, controller_function: Callable):
        self.controller_function = controller_function


    def __call__(self, request: HTTPRequestHandler):
        adapter = RequestAdapter(request)
        output_format, content_type = self._get_formats(adapter.content_type)

        try:
            payload = adapter.read_payload()
            response = self.controller_function(**payload, output_format=output_format)
            request.send_response(200)
            request.set_headers(content_type)
            adapter.write_response(response)
        except APIException as err:
            request.send_response(err.code)
            request.set_headers()
            adapter.write_response({'message': f'{err}'})
