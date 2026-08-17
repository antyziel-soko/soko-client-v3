import os
import json


class ModpackManager:

    def __init__(self, folder):
        self.folder = folder

    def get_modpacks(self):

        if not os.path.exists(self.folder):
            return []

        packs = []

        for item in os.listdir(self.folder):

            path = os.path.join(self.folder, item)

            if os.path.isdir(path):
                config = os.path.join(path, "modpack.json")

                if os.path.exists(config):
                    packs.append(item)

        return packs

    def get_info(self, name):

        path = os.path.join(self.folder, name, "modpack.json")

        if not os.path.exists(path):
            return None

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                return None

            return json.loads(content)

        except json.JSONDecodeError:
            return None