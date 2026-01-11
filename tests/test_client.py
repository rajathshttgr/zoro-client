from zoro_client.client import ZoroClient


def test_clientinit():

    client = ZoroClient(host="localhost", port=6464)
    assert client.testCall() == "http://localhost:6464"
