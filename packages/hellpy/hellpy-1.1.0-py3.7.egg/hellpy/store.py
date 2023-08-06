from typing import List

import json
import logging

from hellpy import requests
from hellpy.structures import (
    BaseType,
    UrlBuilder,
    GetStatement,
    PutStatement,
    DelStatement,
)


class Store(object):
    """
    Store is the main connector for HellDB from where all the
    reads and writes take place using an API designed to replicate
    the syntax of Latin, the query language developed for HellDB.
    """

    def __init__(self, port: int = 8080, host: str = '127.0.0.1'):

        """ Constructor for Store to build HellDB's url. """

        self.url: str = f'http://{host}:{port}'
        self.url_store: UrlBuilder = UrlBuilder(self.url)

        if not self.ok():
            logging.fatal(f"cannot connect to HellDB instance on {self.url}")

    @staticmethod
    def extract(resp_text: str) -> List[BaseType]:

        """ Helper method to return response's BaseType list generically. """

        response = json.loads(resp_text)
        if len(response['errors']) != 0:
            logging.fatal('\n'.join(response['errors']))
        else:
            return response['results'][0]

    def ok(self) -> bool:

        """ Checks whether HellDB is running healthy. """

        resp = requests.get(self.url_store.status_url)
        return resp == "ok"

    def get(self, *keys: str) -> List[BaseType]:

        """ GET api for reading keys. """

        get_statement = GetStatement(*keys)
        return Store.extract(
            requests.post(
                self.url_store.query_url,
                [get_statement],
            ),
        )

    def delete(self, *keys: str) -> List[BaseType]:

        """ DEL api for deleting key value pairs. """

        del_statement = DelStatement(*keys)
        return Store.extract(
            requests.post(
                self.url_store.query_url,
                [del_statement],
            )
        )

    def put(self, key: str, value: BaseType) -> List[BaseType]:

        """ PUT api for writing value to a key. """

        put_statement = PutStatement(key, value)
        return Store.extract(
            requests.post(
                self.url_store.query_url,
                [put_statement],
            )
        )

    def __len__(self) -> int:

        """ Gets number of key-value pairs in HellDB. """

        return int(requests.get(self.url_store.length_url))
