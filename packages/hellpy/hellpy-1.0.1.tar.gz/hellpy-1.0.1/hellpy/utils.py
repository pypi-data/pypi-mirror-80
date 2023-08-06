from typing import Any


def valid_type(obj: Any) -> bool:
    if type(obj) in (str, int, bool):
        return True
    return type(obj) in (set, list, tuple, frozenset) and all(map(valid_type, obj))
