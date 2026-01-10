<div align="center">

## Zoro Client

A Python client library for [Zoro-DB](https://github.com/rajathshttgr/zoro-db), a vector search engine.

[![PyPI](https://badge.fury.io/py/zoro-client.svg)](https://pypi.org/project/zoro-client/)
[![API Docs](https://img.shields.io/badge/Docs-OpenAPI%203.0-success)](https://github.com/rajathshttgr/zoro-db/blob/main/docs/API_DOCS.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/rajathshttgr/zoro-client/blob/main/LICENSE)

</div>

## Installation

```bash
pip install zoro-client
```

---

## Connecting to Zoro-DB Server

```python
from zoro_client import ZoroClient

client = ZoroClient(host="localhost", port=6464)
# or
client = ZoroClient(url="http://localhost:6464")
```

### Run Zoro-DB locally

```bash
docker run -p 6464:6464 ghcr.io/rajathshttgr/zoro-db:dev
```
