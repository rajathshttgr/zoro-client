class ApiClient:
    def __init__(self, host: str):
        self.host = host

    def request(self):
        return self.host
