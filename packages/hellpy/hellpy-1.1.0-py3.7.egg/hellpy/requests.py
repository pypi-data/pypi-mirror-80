from typing import List

import logging
import urllib.parse
import urllib.request

from .tokens import ILLEGAL
from hellpy.structures import Statement


def get(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        logging.error(e)
        return ILLEGAL


def post(url: str, queries: List[Statement]) -> str:
    values = {'query': '\n'.join(map(str, queries))}
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data)
    try:
        with urllib.request.urlopen(req) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        logging.error(e)
        return ILLEGAL
