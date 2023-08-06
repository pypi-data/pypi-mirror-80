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
from pynidus.base import MLTBase

config = {
    "postgresql": {
        "host": "host",
        "user": "user",
        "password": "password",
        "database": "database"
    },
    "elasticsearch": {
        "host": "host",
        "user": "user",
        "password": "password"
    }
}

class TestClassifier(MLTBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def some_method_fetching_data_from_db(self):
        return self.pg_client.query("SELECT * FROM table LIMIT 1")

    def some_other_method_fetching_data_from_es(self):
        return self.es_client.query(
            index="...",
            body={
                "...": "..."
            }
        )

testclassifier = TestClassifier(
    pg_config = config.get("postgresql"),
    es_config = config.get("elasticsearch")
)
```

### TODO

- Add a dev branch
