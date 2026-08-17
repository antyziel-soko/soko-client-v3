import logging
import requests

logger = logging.getLogger("SokoClient.MinecraftAPI")
DEFAULT_TIMEOUT = 10


class MinecraftAPI:

    VERSION_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

    def get_versions(self):
        try:
            response = requests.get(
                self.VERSION_URL,
                timeout=DEFAULT_TIMEOUT,
            )
            if response.status_code == 200:
                return response.json()
            logger.warning("Minecraft version manifest fetch failed: %s status %s", self.VERSION_URL, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Minecraft version manifest fetch failed: %s", exception)

        return None

    def get_release_versions(self):
        data = self.get_versions()

        if not data:
            return []

        versions = []

        for version in data["versions"]:
            if version["type"] == "release":
                versions.append(version)

        return versions