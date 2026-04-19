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

        payload = {
            "vectors": {
                "size":  dimension,
                "distance": distance.lower(),
            }
        }

        return self.api.create_collection(collection_name, payload)

    def recreate_collection(self, collection_name, distance, dimension=100):

        error = self._validate_collection_args(collection_name, distance, dimension)

        if error:
            return {"error": error}

        existing = self.api.get_collection(collection_name).get("result")
        if existing:
            self.api.delete_collection(collection_name)

        payload = {
            "vectors": {
                "size":  dimension,
                "distance": distance.lower(),
            }
        }

        return self.api.create_collection(collection_name, payload)

    def delete_collection(self, collection_name):

        if len(collection_name)==0:
            return {"error": "Collection Name Cannot be empty string"}

        return self.api.delete_collection(collection_name)

    def list_collection(self):
        # list collections
        return self.api.list_collections()

    def upsert_points(self, collection_name, vectors, ids, payloads):

        if len(collection_name)==0:
            return {"error": "Collection Name Cannot be empty string"}
        
        if any(len(v) ==0 for v in vectors):
            return {"error": f"Vectors cannot be empty"}
        
        if any(i<0 for i in ids):
            return {"error": f"Only unsigned integers are allowed as point ID"}

        try:
            vectors = self._normalize_vectors(vectors)
        except (TypeError, ValueError) as e:
            return {"error": str(e)}

        Points=[]

        for i in range(len(ids)):
            point = {
                "id": ids[i],
                "vector": vectors[i],
            }
            # handle payloads if provided
            if payloads:
                point["payload"] = payloads[i]
            else:
                point["payload"] = None

            Points.append(point)

        body = {"points":Points}        

        return self.api.upsert_points(collection_name, body)

    def delete_points(self, collection_name, ids):

        if len(collection_name)==0:
            return {"error": "Collection Name Cannot be empty string"}

        if not ids:
            return {"error": "IDs required"}
        
        if any(i<0 for i in ids):
            return {"error": f"Only unsigned integers are allowed as point ID"}

        return self.api.delete_points(collection_name, {"ids": ids})
    

    def search_query(self, collection_name, query_vector, limit=1):

        if len(collection_name)==0:
            return {"error": "Collection Name Cannot be empty string"}

        #  Normalize numpy arrays
        if isinstance(query_vector, np.ndarray):
            query_vector = query_vector.tolist()

        # Validate type after normalization
        if not isinstance(query_vector, list):
            return {"error": "query_vector must be a list or numpy array"}
        
        if limit > 100 :
            return {"error": "max search query results set limit of 100 for standard retrival"}

        return self.api.search_points(
            collection_name,
            {"vectors": query_vector, "limit": limit},
        )
