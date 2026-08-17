import logging
import os
import shutil
import zipfile

logger = logging.getLogger("SokoClient.ModpackImporter")


class ModpackImporter:

    def import_pack(self, zip_file, destination):

        if not os.path.exists(zip_file):
            return False

        os.makedirs(
            destination,
            exist_ok=True
        )

        base_destination = os.path.abspath(destination)

        try:
            with zipfile.ZipFile(
                zip_file,
                "r"
            ) as zip_ref:
                for member in zip_ref.infolist():
                    member_path = os.path.abspath(os.path.join(destination, member.filename))
                    if not member_path.startswith(base_destination + os.sep) and member_path != base_destination:
                        logger.warning("Skipping suspicious zip entry: %s", member.filename)
                        continue
                    if member.is_dir():
                        os.makedirs(member_path, exist_ok=True)
                        continue
                    os.makedirs(os.path.dirname(member_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(member_path, "wb") as target:
                        shutil.copyfileobj(source, target)
            return True
        except (zipfile.BadZipFile, OSError) as exception:
            logger.warning("Failed to import modpack %s: %s", zip_file, exception)
            return False
