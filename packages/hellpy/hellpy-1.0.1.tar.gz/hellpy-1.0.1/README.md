# HellPy

HellPy is a connector for HellDB - a key value store database.

## Installation

Install it using pip.

```shell script
$ pip install hellpy
```

## Documentation

### Initialize

```python
from hellpy import Store

store = Store()

# To connect to different service.
remote = Store(port=5555, host='222.31.43.43')
```

### PUT

Writes using a PUT call to the HellDB instance store connected to.

```python
store.put('age', 18)
store.put('name', 'Manan')
store.put('posts', [1, 2, 'not found'])
store.put('bitmap', [
    [False, False, True],
    [False, True, False],
    [True, False, False],
])
```

### GET

Reads using a GET call.

```python
store.get('name')
# returns ["Manan"]
store.get('name', 'age')
# returns ["Manan", 18]
store.get('invalid_key')
# returns [None]
```

### DEL

Deletes pair using a DEL call

```python
store.delete('name', 'age')
# returns [{'bool': True}, {'bool': True}]
store.delete('invalid_key')
# returns [{'bool': False}]
```
