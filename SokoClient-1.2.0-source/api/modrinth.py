import logging
import requests

logger = logging.getLogger("SokoClient.Modrinth")


class ModrinthAPI:

    API = "https://api.modrinth.com/v2"
    HEADERS = {"User-Agent": "SokoClient/1.2.0"}

    def search_mods(self, query):

        url = f"{self.API}/search"
        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                params={"query": query},
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            logger.warning("Modrinth search failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Modrinth search failed: %s", exception)

        return []

    def get_project(self, project_id):

        url = f"{self.API}/project/{project_id}"
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            if response.status_code == 200:
                return response.json()
            logger.warning("Modrinth project fetch failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Modrinth project fetch failed: %s", exception)

        return None

    def get_versions(self, project_id, game_version=None, loader=None):

        url = f"{self.API}/project/{project_id}/version"

        params = {}

        if game_version:
            params["game_versions"] = f'["{game_version}"]'

        if loader:
            params["loaders"] = f'["{loader}"]'

        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                params=params,
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            logger.warning("Modrinth versions fetch failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Modrinth versions fetch failed: %s", exception)

        return []
