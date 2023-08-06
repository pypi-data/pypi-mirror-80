# pynidus

[![Build Status](https://travis-ci.org/appchoose/pynidus.svg?branch=master)](https://travis-ci.org/appchoose/pynidus)
[![Coverage status](https://codecov.io/gh/appchoose/pynidus/branch/master/graph/badge.svg)](https://codecov.io/github/appchoose/pynidus?branch=master)
[![PyPI](https://img.shields.io/pypi/dm/pynidus.svg)](https://pypi.python.org/pypi)
[![PyPI](https://img.shields.io/pypi/v/pynidus.svg)](https://pypi.python.org/pypi)

A handful of utilities predominantly made to develop basic Cloud Run services that connect to
the same databases. Any configuration variable should be passed as an environment variable from Cloud Run.

### Usage

Training a ML model usually require multiple databases access. Although it is doable to instantiate a connection to `Postgresql` or `Elasticsearch` everytime one needs to, it can actually become quickly cumbersome to do it for a certain number or models. To make everything a tiny bit more DRY, `pynidus` wraps very small chunks of code to deal with config files and clients instantiation.

```python
from pynidus.base import MultiClient

config = {
    "pg_dev": {
        "host": "host",
        "user": "user",
        "password": "password",
        "database": "database",
        "port": 5432
    },
    "pg_logs": {
        "host": "host",
        "user": "user",
        "password": "password"
        "database": "database"
    },
    "es_dev": {
        "host": "host",
        "user": "user",
        "password": "password"
    }
}

mc = MultiClient(config)
mc.pg_client["logs"].query("SELECT * FROM some_table")
mc.pg_client["dev"].query("SELECT * FROM another_table")
```

Or if you want to use it inside a custom Class:

```python
class CustomClass(MultiClient):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

cc.pg_client["logs"].query("SELECT * FROM some_table")
cc.pg_client["dev"].query("SELECT * FROM another_table")
```

### TODO

- Add a dev branch
