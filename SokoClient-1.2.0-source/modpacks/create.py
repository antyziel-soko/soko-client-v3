import os
import json


class ModpackCreator:

    def create(self, name, version, loader, path):

        os.makedirs(
            path,
            exist_ok=True
        )

        data = {
            "name": name,
            "minecraft_version": version,
            "loader": loader,
            "mods": []
        }

        with open(
            os.path.join(path, "modpack.json"),
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

        return True