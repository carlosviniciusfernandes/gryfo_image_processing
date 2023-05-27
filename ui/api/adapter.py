import json

from functools import cached_property
from requests_toolbelt import MultipartDecoder

from .protocols import HTTPRequestHandler


class RequestAdapter:

    request: HTTPRequestHandler

    def __init__(self, request) -> None:
        self.request = request

    @cached_property
    def data(self):
        length = int(self.request.headers.get('content-length'))
        return self.request.rfile.read(length)

    @cached_property
    def content_type(self):
        return self.request.headers.get('content-type')

    def read_payload(self) -> dict:
        if 'json' in self.content_type:
            return JsonAdapter.read_message_body(self.data)

        if 'multipart/form-data' in self.content_type:
            return MultipartAdapter.read_message_body(self.data, self.content_type)

    def write_response(self, response) -> None:
        if type(response) == dict:
            self.request.wfile.write(json.dumps(response).encode('utf-8'))
            return

        self.request.wfile.write(response)


class JsonAdapter:
    def read_message_body(payload: bytes) -> dict:
        return json.loads(payload)


class MultipartAdapter:
    def read_message_body(payload: bytes, content_type: str) -> dict:
        parsed_data = {}
        for part in MultipartDecoder(payload, content_type).parts:
            params = {}
            disposition = part.headers[b'Content-Disposition']
            for dispPart in str(disposition).split(';'):
                kv = dispPart.split('=', 2)
                params[str(kv[0]).strip()] = str(kv[1]).strip('\"\'\t \r\n') if len(kv)>1 else str(kv[0]).strip()

            type = part.headers[b'Content-Type'] if b'Content-Type' in part.headers else None
            parsed_data[params['name']] = part.content.decode('utf-8').split(',') if not type else part.content

        return parsed_data
