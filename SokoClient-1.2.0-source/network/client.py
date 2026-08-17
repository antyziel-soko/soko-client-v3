import logging
import requests

logger = logging.getLogger("SokoClient.Network")
DEFAULT_TIMEOUT = 10


class NetworkClient:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None, timeout=DEFAULT_TIMEOUT):
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=timeout,
            )
            return response
        except requests.RequestException as exception:
            logger.warning("Network GET failed: %s %s", url, exception)
            return None

    def download(self, url, timeout=DEFAULT_TIMEOUT):
        try:
            response = self.session.get(
                url,
                timeout=timeout,
                stream=True,
            )
            if response.status_code == 200:
                return response.content
            logger.warning("Network download failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Network download failed: %s %s", url, exception)
        return None
