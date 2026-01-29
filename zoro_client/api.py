class APIService:
    def __init__(self, client):
        self.client = client

    # Collections
    def get_collection(self, name):
        return self.client.get(f"/collections/{name}")

    def list_collections(self):
        return self.client.get("/collections/")

    def create_collection(self, payload):
        return self.client.post("/collections/", payload)

    def delete_collection(self, name):
        return self.client.delete(f"/collections/{name}")

    # Points
    def upsert_points(self, collection_name, payload):
        return self.client.post(f"/collections/{collection_name}/points", payload)

    def delete_points(self, collection_name, payload):
        return self.client.delete(f"/collections/{collection_name}/points", payload)

    def search_points(self, collection_name, payload):
        return self.client.post(
            f"/collections/{collection_name}/points/search", payload
        )
