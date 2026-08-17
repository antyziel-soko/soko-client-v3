import os
import minecraft_launcher_lib


class NeoForgeInstaller:

    def __init__(self, minecraft_directory):
        self.minecraft_directory = minecraft_directory

    def find_version(self, minecraft_version):

        try:
            versions = minecraft_launcher_lib.neoforge.list_neoforge_versions()
        except Exception:
            return None

        # wersje NeoForge dla 1.21.4 nazywają się np. "21.4.x"
        prefix = minecraft_version.split(".", 1)[-1] if minecraft_version.startswith("1.") else minecraft_version

        matching = [v for v in versions if v.startswith(prefix)]

        if matching:
            return matching[-1]

        return None

    def install(self, neoforge_version, java_bin_folder=None):

        env_backup = None

        if java_bin_folder:
            env_backup = os.environ.get("PATH", "")
            os.environ["PATH"] = java_bin_folder + os.pathsep + env_backup

        try:
            minecraft_launcher_lib.neoforge.install_neoforge_version(
                neoforge_version,
                self.minecraft_directory
            )
        finally:
            if java_bin_folder and env_backup is not None:
                os.environ["PATH"] = env_backup