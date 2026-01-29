# Supported Methods

| Method                      | Explanation                                                |
| --------------------------- | ---------------------------------------------------------- |
| **Self-Managed embeddings** | You generate vectors yourself and store them, full control |
| **Zoro-managed embeddings** | You pass text, Zoro handles embeddings internally          |

## Installation

```bash
pip install zoro-client
```

## Connecting to Zoro

```python
from zoro_client import ZoroClient

# Local server
client = ZoroClient(host="localhost", port=6464)

# OR using full URL
client = ZoroClient(url="http://localhost:6464")
```

### Run Zoro locally

```bash
docker run -p 6464:6464 ghcr.io/rajathshttgr/zoro-db:dev
```

## Self-Managed Embeddings

You generate embeddings yourself and store raw vectors.

```python
import numpy as np
from zoro_client import VectorConfig, Distance

# Create collection
client.create_collection(
    collection_name="test",
    vector_config=VectorConfig(size=100, distance=Distance.COSINE),
)

# Upsert points
vectors = np.random.rand(5, 100).tolist()

payloads = [
    {"document": "LangChain integration"},
    {"document": "LlamaIndex integration"},
    {"document": "Hybrid search"},
    {"document": "Fast ANN search"},
    {"document": "Python for Machine Learning"},
]

client.upsert_points(
    collection_name="test",
    vectors=vectors,
    ids=[12, 4, 34, 23, 2],
    payloads=payloads,
)

# search query
results = client.search(
    collection_name="test", query_vector=np.random.rand(100).tolist(), limit=2
)

print(results)

```

### Additional methods

```python
# Recreate collection if collection already exists
response = client.recreate_collection(
    collection_name="test",
    vector_config=VectorConfig(size=100, distance=Distance.COSINE),
)

# delete existing collection
response = client.delete_collection(collection_name="test")

# list all collections
print(client.list_collections())

# delete points
response = client.delete_points(collection_name="test", ids=[12, 4, 34])
```

## Zoro-Managed Embeddings

Zoro generates embeddings internally using your API key.

```python
from zoro_client import EmbeddingModelConfig, VectorConfig, Distance, TextInput

# Configure embedding model
embedding_model = EmbeddingModelConfig(
    provider="openai",
    model="text-embedding-3-small",
    api_key="your-api-key"
)

# Create collection
client.create_collection(
    name="docs",
    vector_config=VectorConfig(
        size=client.embedding_size(embedding_model),
        distance=Distance.COSINE
    )
)

# Upsert points
client.upsert(
    collection="docs",
    vectors=[
        TextInput(text="Zoro with LangChain", model=embedding_model),
        TextInput(text="Zoro with LlamaIndex", model=embedding_model)
    ]
)

# Search
results = client.search(
    collection="docs",
    query_vector=TextInput(text="Vector DB integrations", model=embedding_model),
    limit=3
)

print(results)
```
