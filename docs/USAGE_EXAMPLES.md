# Supported Methods

| Method                      | Explanation                                                |
| --------------------------- | ---------------------------------------------------------- |
| **Zoro-managed embeddings** | You pass text, Zoro handles embeddings internally          |
| **Self-Managed embeddings** | You generate vectors yourself and store them, full control |

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

## Zoro-Managed Embeddings

Zoro generates embeddings internally using your API key.

```python
from zoro_client.models import EmbeddingModelConfig, VectorConfig, Distance, TextInput

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

# Insert documents
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
    query=TextInput(text="Vector DB integrations", model=embedding_model),
    limit=3
)

print(results)
```

## Self-Managed Embeddings

You generate embeddings yourself and store raw vectors.

```python
import numpy as np
from zoro_client.models import VectorConfig, Distance, Point

# Create collection
client.create_collection(
    name="vectors",
    vector_config=VectorConfig(size=100, distance=Distance.COSINE)
)

# Insert vectors

vectors = np.random.rand(4, 100)

payloads = [
    {"document": "LangChain integration"},
    {"document": "LlamaIndex integration"},
    {"document": "Hybrid search"},
    {"document": "Fast ANN search"},
]

points = [
    Point(
        id=i,
        vector=v.tolist(),
        payload=payloads[i],
    )
    for i, v in enumerate(vectors)
]

client.upsert(collection="vectors", points=points)

# Search
results = client.search(
    collection="vectors",
    vector=np.random.rand(100),
    limit=2
)

print(results)
```
