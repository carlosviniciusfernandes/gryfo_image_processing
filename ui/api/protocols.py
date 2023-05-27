from typing import Protocol


class HTTPRequestHandler(Protocol):
    def do_POST(self):
        ...

    def set_headers(self, type:str):
        ...
