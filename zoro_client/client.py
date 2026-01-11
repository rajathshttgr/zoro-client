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

    def testCall(self):
        return self.url
