import requests


class HTTPClient:
    def __init__(self, url):
        self.url = url

    def get(self, endpoint="/"):
        url_path = self.url + endpoint
        response = requests.get(url_path)

        return response.json()

    def post(self, endpoint="/", body={}):
        url_path = self.url + endpoint

        response = requests.post(url_path, json=body)

        return response.json()

    def delete(self, endpoint="/", body={}):
        url_path = self.url + endpoint
        response = requests.delete(url_path, json=body)

        return response.json()

    def create_collection(self, collection_name="", distance="", dimension=100):
        if dimension <= 0 or dimension > 9999:
            print("Ideal dimension range is 1 to 9999")
            return False

        distance_enum = ["cosine", "dot", "l2"]
        isValid = False
        for dist in distance_enum:
            if dist == distance.lower():
                isValid = True

        if not isValid:
            print("Enter valid distance matrics COSINE/DOT/L2")
            return False

        if len(collection_name) < 1 or len(collection_name) > 36:
            print(
                "Invalid collection name, enter collection name of 1 to 36 character long"
            )
            return False

        # get collection
        response = self.get(endpoint=f"/collections/{collection_name}")

        result = response.get("result")

        if result and result.get("collection_name") == collection_name:
            print("Collection name already exists, please delete to recreate.")
            return False

        # create collection
        payload = {
            "collection_name": collection_name,
            "dimension": dimension,
            "distance": distance.lower(),
        }

        response = self.post("/collections/", body=payload)

        return True

    def recreate_collection(self, collection_name="", distance="", dimension=100):
        if dimension <= 0 or dimension > 9999:
            print("Ideal dimension range is 1 to 9999")
            return False

        distance_enum = ["cosine", "dot", "l2"]
        isValid = False
        for dist in distance_enum:
            if dist == distance.lower():
                isValid = True

        if not isValid:
            print("Enter valid distance matrics COSINE/DOT/L2")
            return False

        if len(collection_name) < 1 or len(collection_name) > 36:
            print(
                "Invalid collection name, enter collection name of 1 to 36 character long"
            )
            return False

        # get collection
        response = self.get(endpoint=f"/collections/{collection_name}")

        result = response.get("result")

        if result and result.get("collection_name") == collection_name:
            # if collection already exists delete
            response = self.delete(endpoint=f"/collections/{collection_name}")
            result_data = response.get("result")
            if result_data and result_data.get("collection_name") == collection_name:
                pass
            else:
                print("failed to delete the existing collection")
                return False

        # create collection
        payload = {
            "collection_name": collection_name,
            "dimension": dimension,
            "distance": distance.lower(),
        }

        response = self.post("/collections/", body=payload)

        # if success return true

        return True

    def delete_collection(self, collection_name=""):
        # get collection
        response = self.get(endpoint=f"/collections/{collection_name}")

        result = response.get("result")

        if result and result.get("collection_name") == collection_name:
            # if collection already exists delete
            response = self.delete(endpoint=f"/collections/{collection_name}")
            result_data = response.get("result")
            if result_data and result_data.get("collection_name") == collection_name:
                print("Collection deleted successfully")
                return True
            else:
                print("failed to delete the existing collection")
                return False
        else:
            print("Collection doesn't exist in the database")
            return False

    def list_collection(self):
        # list collections
        response = self.get(endpoint=f"/collections/")
        return response

    def upsert_points(self, collection_name="", vectors=[], ids=[], payload={}):
        response = self.get(endpoint=f"/collections/{collection_name}")
        result = response.get("result")
        if result == None:
            return {"error": "failed to retrive collection info"}

        if result and result.get("collection_name") != collection_name:
            return {"error": "collection not found"}

        dimension = int(result.get("dimension"))

        if len(vectors[0]) != dimension:
            return {"error": f"expected vector dimension is {dimension}"}
        else:
            for v in vectors:
                if len(v) != dimension:
                    return {"error": "inconsistent vectors dimension"}

        if len(vectors) == len(ids) == len(payload):
            pass
        else:
            return {
                "error": "id counts doesn't match with vector size and payload size"
            }

        # upsert points
        payload = {
            "vectors": vectors,
            "ids": ids,
            "payload": payload,
        }

        response = self.post(f"/collections/{collection_name}/points", body=payload)

        result = response.get("result")

        if result == None:
            return {"error": "something went wrong"}

        if result and result.get("status") == "success":
            return {"message": "Points upsert successfull", "result": result}
        else:
            error_message = result.get("error")
            return {"error": error_message}

    def delete_points(self, collection_name="", ids=[]):
        get_response = self.get(endpoint=f"/collections/{collection_name}")
        result = get_response.get("result")
        if result == None:
            return {"error": "failed to retrive collection info"}

        if result and result.get("collection_name") != collection_name:
            return {"error": "collection not found"}

        if len(ids) < 1:
            return {"error": "Please include points IDs to delete"}

        # delete points
        payload = {"ids": ids}

        delete_response = self.delete(
            endpoint=f"/collections/{collection_name}/points", body=payload
        )

        result = delete_response.get("result")

        if result == None:
            return {"error": "something went wrong"}

        if result and result.get("status") == "success":
            return {"message": "Points deleted successfully", "result": result}
        else:
            error_message = result.get("error")
            return {"error": error_message}
