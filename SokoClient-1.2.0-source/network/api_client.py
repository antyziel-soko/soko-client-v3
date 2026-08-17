from network.client import NetworkClient


class APIClient:

    def __init__(self):
        self.client = NetworkClient()


    def get_json(self, url, params=None):

        response = self.client.get(
            url,
            params
        )

        if response:

            try:
                return response.json()

            except Exception:
                return None

        return None


    def get_text(self, url):

        response = self.client.get(
            url
        )

        if response:
            return response.text

        return None