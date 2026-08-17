import logging
import os
import requests

logger = logging.getLogger("SokoClient.ModUpdater")
DEFAULT_TIMEOUT = 20


class ModUpdater:

    def update(self, mod_file, new_url):

        if not os.path.exists(mod_file):
            return False

        try:
            response = requests.get(new_url, timeout=DEFAULT_TIMEOUT)
            if response.status_code != 200:
                logger.warning("Mod update failed %s: status %s", new_url, response.status_code)
                return False

            with open(mod_file, "wb") as file:
                file.write(response.content)

            return True
        except requests.RequestException as exception:
            logger.warning("Mod update failed %s: %s", new_url, exception)
            return False