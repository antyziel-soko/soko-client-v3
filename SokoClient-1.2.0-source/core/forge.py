import os
import minecraft_launcher_lib


class ForgeInstaller:

    def __init__(self, minecraft_directory):
        self.minecraft_directory = minecraft_directory

    def find_version(self, minecraft_version):

        try:
            return minecraft_launcher_lib.forge.find_forge_version(
                minecraft_version
            )
        except Exception:
            return None

    def is_supported(self, forge_version):

        try:
            return minecraft_launcher_lib.forge.supports_automatic_install(
                forge_version
            )
        except Exception:
            return False

    def install(self, forge_version, java_bin_folder=None):

        env_backup = None

        if java_bin_folder:
            env_backup = os.environ.get("PATH", "")
            os.environ["PATH"] = java_bin_folder + os.pathsep + env_backup

        try:
            minecraft_launcher_lib.forge.install_forge_version(
                forge_version,
                self.minecraft_directory
            )
        finally:
            if java_bin_folder and env_backup is not None:
                os.environ["PATH"] = env_backup