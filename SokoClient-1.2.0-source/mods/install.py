import logging
import os
import requests

logger = logging.getLogger("SokoClient.ModInstaller")


class ModInstaller:

    def __init__(self, mods_folder):
        self.mods_folder = mods_folder

    def install(self, url, filename):

        os.makedirs(
            self.mods_folder,
            exist_ok=True
        )

        filename = os.path.basename(filename)
        path = os.path.join(
            self.mods_folder,
            filename
        )

        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                with open(path, "wb") as file:
                    file.write(response.content)
                return True
            logger.warning("Mod download failed (%s): status %s", url, response.status_code)
        except requests.RequestException as exception:
            logger.warning("Mod download failed (%s): %s", url, exception)

        return False
