from zoro_client import ZoroClient

# Local server
client = ZoroClient(host="localhost", port=6464)

import numpy as np
from zoro_client import VectorConfig, Distance

# Create collection
client.recreate_collection(
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
