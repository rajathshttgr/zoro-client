import requests


class HTTPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _handle_response(self, response: requests.Response):
        try:
            return response.json()
        except ValueError:
            raise RuntimeError(
                f"Non-JSON response ({response.status_code}): {response.text}"
            )

    def get(self, endpoint: str):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        resp = requests.get(url)
        return self._handle_response(resp)

    def post(self, endpoint: str, body=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        resp = requests.post(url, json=body or {})

        return self._handle_response(resp)

    def delete(self, endpoint: str, body=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        resp = requests.delete(url, json=body or {})
        return self._handle_response(resp)
