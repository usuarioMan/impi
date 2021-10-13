import json
from types import Union

from pymongo.collection import Collection
from aiohttp import FormData


class HTTPMessage:
    def __repr__(self):
        return ', '.join([f"{k} -> {v}" for k, v in self.__dict__.items()])


class MessageBuilder:
    """
    Constructor para mensajes HTTP. Nunca usar directamente.

    """

    def __init__(self):
        self._url = None
        self._method = None
        self._headers = None
        self._body = None
        self._page = None
        self._search = None

        self._request = None

    def build_url(self, url: str):
        self._url = url
        return self

    def build_method(self, method):
        self._method = method
        return self

    def build_headers(self, headers):
        self._headers = headers
        return self

    def build_body(self, body, *args, **kwargs):
        self._body = body
        return self


class GeneralPost(MessageBuilder):
    def build_method(self, method="POST"):
        self._method = method
        return self

    def build_body(self, body, *args, **kwargs):
        search_filter = locals()['kwargs']
        body.update(search_filter)
        self._body = body
        return self

    def build(self):
        r = HTTPMessage()
        r.url = self._url
        r.method = self._method
        r.headers = self._headers
        r.body = self._body
        return r


class GeneralGet(MessageBuilder):
    def build_method(self, method="GET"):
        self._method = method
        return self

    def build(self):
        r = HTTPMessage()
        r.url = self._url
        r.method = self._method
        r.headers = self._headers
        r.body = self._body
        return r


def general_post(data: Collection, page, search) -> HTTPMessage:
    message = GeneralPost() \
        .build_url(data['url']) \
        .build_method() \
        .build_headers(data['headers']) \
        .build_body(data['body'], numeroPagina=page, contenido=search) \
        .build()

    return message


def general_get(data: Union[Collection, dict]) -> HTTPMessage:
    message = GeneralPost() \
        .build_url(data['url']) \
        .build_method() \
        .build_headers(data['headers']) \
        .build()

    return message
