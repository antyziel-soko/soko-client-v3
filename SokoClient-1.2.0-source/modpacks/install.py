import os
import shutil
import json


class ModpackInstaller:

    def install(self, modpack_path, game_folder):

        if not os.path.exists(modpack_path):
            return False

        os.makedirs(
            game_folder,
            exist_ok=True
        )

        config = os.path.join(
            modpack_path,
            "modpack.json"
        )

        if os.path.exists(config):
            shutil.copy(
                config,
                game_folder
            )

        mods = os.path.join(
            modpack_path,
            "mods"
        )

        if os.path.exists(mods):
            shutil.copytree(
                mods,
                os.path.join(game_folder, "mods"),
                dirs_exist_ok=True
            )

        return True