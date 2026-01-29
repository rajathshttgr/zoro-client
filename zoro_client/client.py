from .http_client import HTTPClient
from .api import APIService
from .service import CollectionService


class ZoroClient:
    def __init__(self, host=None, port=None, url=None):
        self.port = port
        self.host = host
        self.url = url
        if url is None:
            if host is None:
                self.host = "localhost"
            if port is None:
                self.port = 6464
            self.url = f"http://{host}:{port}"

        client = HTTPClient(self.url)
        api = APIService(client)
        self.collection = CollectionService(api)

    def create_collection(self, collection_name, vector_config):
        dimension = vector_config.dimension
        distance = vector_config.distance
        return self.collection.create_collection(
            collection_name=collection_name,
            dimension=dimension,
            distance=distance,
        )

    def recreate_collection(self, collection_name, vector_config):
        dimension = vector_config.dimension
        distance = vector_config.distance
        return self.collection.recreate_collection(
            collection_name=collection_name,
            dimension=dimension,
            distance=distance,
        )

    def delete_collection(self, collection_name):
        return self.collection.delete_collection(
            collection_name=collection_name,
        )

    def list_collections(self):
        """Add filter by dimension, distance, name starting with and name ending with ex. `%ies` or `mov%`"""
        return self.collection.list_collection()

    def upsert_points(self, collection_name, vectors, ids, payloads):

        return self.collection.upsert_points(
            collection_name=collection_name,
            vectors=vectors,
            ids=ids,
            payloads=payloads,
        )

    def delete_points(self, collection_name, ids):
        return self.collection.delete_points(collection_name=collection_name, ids=ids)

    def search(self, collection_name, query_vector, limit=1):
        return self.collection.search_query(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
        )
