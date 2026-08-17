import os
import shutil


class ModService:

    def __init__(self, mods_folder):
        self.mods_folder = mods_folder


    def get_mods(self):

        if not os.path.exists(self.mods_folder):
            return []

        return [
            file for file in os.listdir(self.mods_folder)
            if file.endswith(".jar")
        ]


    def remove_mod(self, name):

        path = os.path.join(
            self.mods_folder,
            name
        )

        if os.path.exists(path):
            os.remove(path)
            return True

        return False


    def backup_mod(self, name, backup_folder):

        source = os.path.join(
            self.mods_folder,
            name
        )

        if os.path.exists(source):

            os.makedirs(
                backup_folder,
                exist_ok=True
            )

            shutil.copy(
                source,
                backup_folder
            )

            return True

        return False