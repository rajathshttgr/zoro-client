import numpy as np


class CollectionService:
    def __init__(self, api):
        self.api = api

    def _validate_collection_args(self, name, distance, dimension):
        if not (1 <= len(name) <= 36):
            return "Collection name must be 1–36 characters"

        VALID_DISTANCES = {"cosine", "dot", "l2"}
        if distance.lower() not in VALID_DISTANCES:
            return "Distance must be cosine, dot, or l2"

        if dimension <= 0 or dimension > 9999:
            return "Dimension must be between 1 and 9999"

        return None

    def _normalize_vectors(self, vectors):
        """
        Accepts:
        - List[List[float]]
        - np.ndarray (2D)


        Returns:
        - List[List[float]]
        """

        if isinstance(vectors, np.ndarray):
            if vectors.ndim != 2:
                raise ValueError("Vectors ndarray must be 2-dimensional")
            return vectors.tolist()

        if isinstance(vectors, list):
            if not all(isinstance(v, list) for v in vectors):
                raise TypeError("Vectors must be a list of lists")
            return vectors

        raise TypeError("Vectors must be a list of lists or a numpy ndarray")

    def create_collection(self, collection_name, distance, dimension=100):

        error = self._validate_collection_args(collection_name, distance, dimension)

        if error:
            return {"error": error}

        existing = self.api.get_collection(collection_name).get("result")

        if existing:
            return {"error": "Collection already exists"}

        payload = {
            "collection_name": collection_name,
            "dimension": dimension,
            "distance": distance.lower(),
        }

        return self.api.create_collection(payload)

    def recreate_collection(self, collection_name, distance, dimension=100):

        error = self._validate_collection_args(collection_name, distance, dimension)

        if error:
            return {"error": error}

        existing = self.api.get_collection(collection_name).get("result")
        if existing:
            self.api.delete_collection(collection_name)

        payload = {
            "collection_name": collection_name,
            "dimension": dimension,
            "distance": distance.lower(),
        }

        return self.api.create_collection(payload)

    def delete_collection(self, collection_name):

        existing = self.api.get_collection(collection_name).get("result")
        if not existing:
            return {"error": "Collection not found"}

        return self.api.delete_collection(collection_name)

    def list_collection(self):
        # list collections
        return self.api.list_collections()

    def upsert_points(self, collection_name, vectors, ids, payloads):

        collection = self.api.get_collection(collection_name).get("result")
        if not collection:
            return {"error": "Collection not found"}

        dim = int(collection["dimension"])

        try:
            vectors = self._normalize_vectors(vectors)
        except (TypeError, ValueError) as e:
            return {"error": str(e)}

        if any(len(v) != dim for v in vectors):
            return {"error": f"Vector dimension must be {dim}"}

        if not (len(vectors) == len(ids) == len(payloads)):
            return {"error": "Vectors, ids and payload size mismatch"}

        body = {
            "vectors": vectors,
            "ids": ids,
            "payload": payloads,
        }

        return self.api.upsert_points(collection_name, body)

    def delete_points(self, collection_name, ids):
        collection = self.api.get_collection(collection_name).get("result")
        if not collection:
            return {"error": "Collection not found"}

        if not ids:
            return {"error": "IDs required"}

        return self.api.delete_points(collection_name, {"ids": ids})

    def search_query(self, collection_name, query_vector, limit=1):

        collection = self.api.get_collection(collection_name).get("result")
        if not collection:
            return {"error": "Collection not found"}

        #  Normalize numpy arrays
        if isinstance(query_vector, np.ndarray):
            query_vector = query_vector.tolist()

        # Validate type after normalization
        if not isinstance(query_vector, list):
            return {"error": "query_vector must be a list or numpy array"}

        if len(query_vector) != int(collection["dimension"]):
            return {"error": "Vector dimension mismatch"}

        return self.api.search_points(
            collection_name,
            {"vectors": query_vector, "limit": limit},
        )
