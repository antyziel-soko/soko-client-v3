import logging
import requests

logger = logging.getLogger("SokoClient.Updater")
CHECK_TIMEOUT = 8
DOWNLOAD_TIMEOUT = 20


class Updater:
    def __init__(self, current_version):
        self.current_version = current_version

    def check(self, url):
        if not url:
            return None
        try:
            response = requests.get(url, timeout=CHECK_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else None
        except requests.RequestException as exception:
            logger.warning("Update check failed: %s", exception)
        except ValueError as exception:
            logger.warning("Update check parse failed: %s", exception)

        return None

    def is_newer(self, version):
        def parts(value):
            return tuple(int(part) if part.isdigit() else 0 for part in str(value).split("."))
        return bool(version) and parts(version) > parts(self.current_version)

    def download_update(self, url, file, progress=None):
        try:
            with requests.get(url, timeout=DOWNLOAD_TIMEOUT, stream=True) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))
                downloaded = 0
                with open(file, "wb") as handle:
                    for chunk in response.iter_content(65536):
                        if chunk:
                            handle.write(chunk)
                            downloaded += len(chunk)
                            if progress and total:
                                progress(downloaded / total)
            return True
        except requests.RequestException as exception:
            logger.warning("Update download failed: %s", exception)
        except OSError as exception:
            logger.warning("Update file write failed: %s", exception)

        return False
