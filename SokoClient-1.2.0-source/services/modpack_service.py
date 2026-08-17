import os
import shutil


class ModpackService:

    def __init__(self, folder):
        self.folder = folder


    def get_modpacks(self):

        if not os.path.exists(self.folder):
            return []

        return [
            item for item in os.listdir(self.folder)
            if os.path.isdir(
                os.path.join(
                    self.folder,
                    item
                )
            )
        ]


    def delete_modpack(self, name):

        path = os.path.join(
            self.folder,
            name
        )

        if os.path.exists(path):

            shutil.rmtree(path)

            return True

        return False


    def create_modpack(self, name):

        path = os.path.join(
            self.folder,
            name
        )

        os.makedirs(
            path,
            exist_ok=True
        )

        return path