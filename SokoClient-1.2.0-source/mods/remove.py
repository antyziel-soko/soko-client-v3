import os


class ModRemover:

    def remove(self, mod_file):

        if os.path.exists(mod_file):
            os.remove(mod_file)
            return True

        return False

    def remove_all(self, mods_folder):

        if not os.path.exists(mods_folder):
            return False

        for file in os.listdir(mods_folder):
            if file.endswith(".jar"):
                os.remove(
                    os.path.join(
                        mods_folder,
                        file
                    )
                )

        return True