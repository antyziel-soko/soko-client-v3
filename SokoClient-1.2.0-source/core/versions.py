import minecraft_launcher_lib


class VersionManager:

    def get_all_versions(self):
        return minecraft_launcher_lib.utils.get_available_versions()

    def get_release_versions(self):
        versions = self.get_all_versions()

        return [
            version for version in versions
            if version["type"] == "release"
        ]

    def get_versions_from(self, start_version="1.20.1"):
        versions = self.get_release_versions()

        result = []

        for version in versions:
            if version["id"] >= start_version:
                result.append(version)

        return result