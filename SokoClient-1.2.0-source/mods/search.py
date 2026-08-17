import logging
import requests

logger = logging.getLogger("SokoClient.ModrinthSearch")
DEFAULT_TIMEOUT = 10


class ModrinthSearch:

    API = "https://api.modrinth.com/v2"
    HEADERS = {"User-Agent": "SokoClient/1.2.0"}

    def search(self, query, minecraft_version, loader):

        url = f"{self.API}/search"

        params = {
            "query": query,
            "facets": f'[[\"versions:{minecraft_version}\"],[\"categories:{loader}\"]]'
        }

        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                params=params,
                timeout=DEFAULT_TIMEOUT,
            )
            if response.status_code == 200:
                return response.json()
            logger.warning("Modrinth search failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Modrinth search failed: %s", exception)

        return []
