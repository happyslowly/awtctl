import httpx


class AwtrixClient:
    def __init__(self, host: str):
        self.base = f"http://{host}/api"

    def get(self, path: str):
        return httpx.get(f"{self.base}/{path}").raise_for_status().json()

    def post(self, path: str, payload: dict):
        return httpx.post(f"{self.base}/{path}", json=payload).raise_for_status()
