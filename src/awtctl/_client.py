import httpx


class AwtrixClient:
    def __init__(self, host: str, timeout: float = 10.0):
        self.base = f"http://{host}/api"
        self.timeout = timeout

    def get(self, path: str):
        return httpx.get(f"{self.base}/{path}", timeout=self.timeout).raise_for_status().json()

    def post(self, path: str, payload: dict):
        return httpx.post(f"{self.base}/{path}", json=payload, timeout=self.timeout).raise_for_status()
