from .service import HTTPClient


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

        self.api = HTTPClient(self.url)

    def create_collection(self, collection_name, dimension, distance):
        self.collection_name = collection_name
        self.dimension = dimension
        self.distance = distance
        success = self.api.create_collection(
            collection_name=self.collection_name,
            dimension=self.dimension,
            distance=self.distance,
        )
        if success:
            return {"status": True, "message": "collection created successfully"}
        else:
            return {"status": False, "message": "failed to create collection"}

    def recreate_collection(self, collection_name, dimension, distance):
        self.collection_name = collection_name
        self.dimension = dimension
        self.distance = distance
        success = self.api.recreate_collection(
            collection_name=self.collection_name,
            dimension=self.dimension,
            distance=self.distance,
        )
        if success:
            return {"status": True, "message": "collection recreated successfully"}
        else:
            return {"status": False, "message": "failed to recreate collection"}

    def delete_collection(self, collection_name):
        self.collection_name = collection_name
        success = self.api.delete_collection(
            collection_name=self.collection_name,
        )
        if success:
            return {"status": True, "message": "collection deleted successfully"}
        else:
            return {"status": False, "message": "collection deletion failed"}

    def list_collections(self):
        """Add filter by dimension, distance, name starting with and name ending with ex. `%ies` or `mov%`"""
        return self.api.list_collection()

    def upsert_points(self, collection_name="", vectors=[], ids=[], payload=[]):
        self.collection_name = collection_name
        self.vectors = vectors
        self.ids = ids
        self.payload = payload
        return self.api.upsert_points(
            collection_name=self.collection_name,
            vectors=self.vectors,
            ids=self.ids,
            payload=self.payload,
        )

    def delete_points(self, collection_name="", ids=[]):
        self.collection_name = collection_name
        self.ids = ids
        return self.api.delete_points(
            collection_name=self.collection_name, ids=self.ids
        )
