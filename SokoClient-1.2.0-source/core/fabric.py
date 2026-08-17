import logging
import requests

logger = logging.getLogger("SokoClient.FabricInstaller")
DEFAULT_TIMEOUT = 10


class FabricInstaller:

    FABRIC_META = "https://meta.fabricmc.net/v2"

    def __init__(self, minecraft_directory):
        self.minecraft_directory = minecraft_directory

    def get_loader_versions(self):
        url = f"{self.FABRIC_META}/versions/loader"
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            logger.warning("Fabric loader versions fetch failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Fabric loader versions fetch failed: %s", exception)

        return []

    def get_game_versions(self):
        url = f"{self.FABRIC_META}/versions/game"
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            logger.warning("Fabric game versions fetch failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Fabric game versions fetch failed: %s", exception)

        return []

    def get_installer(self):
        url = f"{self.FABRIC_META}/versions/installer"
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            logger.warning("Fabric installer fetch failed: %s status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Fabric installer fetch failed: %s", exception)

        return []