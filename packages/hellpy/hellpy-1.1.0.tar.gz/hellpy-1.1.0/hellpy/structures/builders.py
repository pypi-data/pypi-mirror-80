import json

from hellpy.utils import valid_type
from hellpy.structures import BaseType
from hellpy.exceptions import InvalidTypeError


class Builder(object):
    pass


class UrlBuilder(Builder):
    def __init__(self, base_url: str) -> None:
        self.query_url = f'{base_url}/query'
        self.status_url = f'{base_url}/status'
        self.length_url = f'{base_url}/length'


class KeyValueBuilder(Builder):
    @staticmethod
    def keys_string(*keys: str) -> str:
        return ' & '.join(keys)

    @staticmethod
    def value_string(value: BaseType) -> str:
        if not valid_type(value):
            raise InvalidTypeError(f'invalid type "{type(value)}" provided')
        return json.dumps(value)
