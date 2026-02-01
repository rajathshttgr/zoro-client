from zoro_client import ZoroClient, VectorConfig, Distance


client = ZoroClient(host="localhost", port=6464)

def test_create_collection():
    client.delete_collection("test")
    response = client.create_collection(collection_name="test", vector_config=VectorConfig(size=4, distance=Distance.COSINE))
    assert "result" in response
    assert response["result"]["collection_name"] == "test"
    assert response["result"]["dimension"] == 4
    assert response["result"]["distance"] == "cosine"


def test_delete_collection():
    client.recreate_collection(collection_name="test", vector_config=VectorConfig(size=4, distance=Distance.COSINE))
    response = client.delete_collection("test")
    assert "result" in response
    assert response["result"]["collection_name"] == "test"


def test_list_collections_basic():
    response = client.list_collections()

    assert "result" in response
    assert isinstance(response["result"], list)

