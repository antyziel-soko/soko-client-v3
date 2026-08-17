import logging
import os
import requests

logger = logging.getLogger("SokoClient.Downloader")
DEFAULT_TIMEOUT = 20


class Downloader:

    def download(self, url, path):
        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        try:
            response = requests.get(
                url,
                stream=True,
                timeout=DEFAULT_TIMEOUT,
            )

            if response.status_code != 200:
                logger.warning("Downloader failed: %s status %s", url, response.status_code)
                return False

            with open(path, "wb") as file:
                for chunk in response.iter_content(1024):
                    if chunk:
                        file.write(chunk)

            return True
        except requests.RequestException as exception:
            logger.warning("Downloader failed: %s", exception)
            return False