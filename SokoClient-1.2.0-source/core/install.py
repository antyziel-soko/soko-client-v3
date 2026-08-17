import minecraft_launcher_lib


class MinecraftInstaller:

    def __init__(self, minecraft_directory):
        self.minecraft_directory = minecraft_directory

    def install(self, version):
        minecraft_launcher_lib.install.install_minecraft_version(
            version,
            self.minecraft_directory
        )

    def is_installed(self, version):
        versions = minecraft_launcher_lib.utils.get_installed_versions(
            self.minecraft_directory
        )

        for item in versions:
            if item["id"] == version:
                return True

        return False