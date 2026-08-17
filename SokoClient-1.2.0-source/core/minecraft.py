import os
import subprocess
import sys
import minecraft_launcher_lib


def get_release_version_ids():
    try:
        return [item["id"] for item in minecraft_launcher_lib.utils.get_version_list() if item.get("type") == "release"]
    except Exception:
        return []


class MinecraftLauncher:
    def __init__(self, minecraft_directory):
        self.minecraft_directory = minecraft_directory
        os.makedirs(self.minecraft_directory, exist_ok=True)

    def get_directory(self): return self.minecraft_directory

    def get_installed_versions(self):
        folder = os.path.join(self.minecraft_directory, "versions")
        if not os.path.isdir(folder): return []
        return sorted((name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))), reverse=True)

    def is_installed(self, version): return version in self.get_installed_versions()

    def install_fabric(self, minecraft_version, fabric_version=None, java_bin_folder=None):
        original = os.environ.get("PATH", "")
        try:
            if java_bin_folder: os.environ["PATH"] = java_bin_folder + os.pathsep + original
            minecraft_launcher_lib.fabric.install_fabric(minecraft_version, self.minecraft_directory, fabric_version)
        finally:
            os.environ["PATH"] = original

    def find_fabric_version_id(self, minecraft_version):
        return next((v for v in self.get_installed_versions() if v.startswith("fabric-loader") and minecraft_version in v), None)

    def find_forge_version_id(self, minecraft_version):
        return next((v for v in self.get_installed_versions() if "neoforge" not in v.lower() and "forge" in v.lower() and minecraft_version in v), None)

    def find_neoforge_version_id(self, minecraft_version):
        return next((v for v in self.get_installed_versions() if v.lower().startswith("neoforge") and minecraft_version in v), None)

    def is_fabric_installed(self, version): return self.find_fabric_version_id(version) is not None
    def is_forge_installed(self, version): return self.find_forge_version_id(version) is not None
    def is_neoforge_installed(self, version): return self.find_neoforge_version_id(version) is not None

    def launch(self, version, username="Player", ram=4, java_path=None, uuid="", access_token="", jvm_arguments="", resolution=None):
        arguments = [f"-Xmx{int(ram)}G"] + [arg for arg in jvm_arguments.split() if arg]
        options = {"username": username, "uuid": uuid, "token": access_token, "jvmArguments": arguments}
        if java_path and java_path != "java": options["executablePath"] = java_path
        if resolution: options.update({"customResolution": True, "resolutionWidth": str(resolution[0]), "resolutionHeight": str(resolution[1])})
        command = minecraft_launcher_lib.command.get_minecraft_command(version, self.minecraft_directory, options)
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        return subprocess.Popen(command, creationflags=flags)

    def launch_fabric(self, minecraft_version, *args, **kwargs):
        version_id = self.find_fabric_version_id(minecraft_version)
        if not version_id: raise RuntimeError("Fabric nie został zainstalowany.")
        return self.launch(version_id, *args, **kwargs)

