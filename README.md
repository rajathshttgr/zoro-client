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

## Self-Managed Embeddings

You generate embeddings yourself and store raw vectors.

```python
from zoro_client import VectorConfig, Distance

# Create collection
client.create_collection(
    collection_name="test",
    vector_config=VectorConfig(size=100, distance=Distance.COSINE)
)

# Upsert points

import numpy as np

vectors = np.random.rand(5, 100).tolist()

payloads = [
    {"document": "LangChain integration"},
    {"document": "LlamaIndex integration"},
    {"document": "Hybrid search"},
    {"document": "Fast ANN search"},
    {"document": "Python for Machine Learning"},
]

response = client.upsert_points(
    collection_name="test",
    vectors=vectors,
    ids=[12, 4, 34, 23, 2],
    payload=payloads,
)


# search query

results = client.search(
    collection_name="test",
    vector=np.random.rand(100),
    limit=2
)

print(results)
```
