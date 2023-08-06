import abc

from hellpy.tokens import *
from hellpy.structures import BaseType
from hellpy.structures import KeyValueBuilder
from hellpy.exceptions import InvalidArgumentError


class Statement(abc.ABC):

    """ A generic Statement class modelled after HellDB's statement interface. """

    @property
    @abc.abstractmethod
    def token(self) -> str:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class GetStatement(Statement):
    def __init__(self, *keys: str):
        if len(keys) == 0:
            raise InvalidArgumentError('at least one key required to read')
        self.keys = keys

    @property
    def token(self) -> str:
        return GET

    def __str__(self) -> str:
        keys_str = " & ".join(self.keys)
        return f'{self.token} {keys_str};'


class DelStatement(Statement):
    def __init__(self, *keys: str):
        if len(keys) == 0:
            raise InvalidArgumentError('at least one key required to delete')
        self.keys_string = KeyValueBuilder.keys_string(*keys)

    @property
    def token(self) -> str:
        return DEL

    def __str__(self) -> str:
        return f'{self.token} {self.keys_string};'


class PutStatement(Statement):
    def __init__(self, key: str, value: BaseType):
        self.key = key
        self.value_string: str = KeyValueBuilder.value_string(value)

    @property
    def token(self) -> str:
        return PUT

    def __str__(self) -> str:
        return f'{self.token} {self.key} {self.value_string};'
