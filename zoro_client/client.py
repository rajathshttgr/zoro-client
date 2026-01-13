from zoro_client.http import ApiClient


class ZoroClient:
    def __init__(
        self,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ):

        if url is None:
            self.url = f"http://{host}:{port}"
        else:
            self.url = url

    def create_collection(self, name: str, vectors_config: str | None = None) -> bool:
        return f"collection {name} created successfully with distance matrix {vectors_config}"

    def testCall(self):
        api = ApiClient(host=self.url)
        return api.request()
