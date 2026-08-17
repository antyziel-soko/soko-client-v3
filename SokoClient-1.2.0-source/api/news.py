import logging
import requests

logger = logging.getLogger("SokoClient.NewsAPI")
DEFAULT_TIMEOUT = 10


class NewsAPI:

    def __init__(self):
        self.url = "https://api.modrinth.com/v2/news"

    def get_news(self):
        try:
            response = requests.get(
                self.url,
                timeout=DEFAULT_TIMEOUT,
            )
            if response.status_code == 200:
                return response.json()
            logger.warning("News fetch failed: %s status %s", self.url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("News fetch failed: %s", exception)

        return []