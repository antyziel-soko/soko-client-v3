import json
import os
import shutil


class ModLibrary:
    """Keeps mod sets apart by loader and Minecraft version."""
    def __init__(self, minecraft_folder): self.minecraft_folder = minecraft_folder
    def folder(self, version, loader):
        safe_loader = "".join(c for c in loader.lower() if c.isalnum() or c in "-_")
        safe_version = "".join(c for c in version if c.isalnum() or c in ".-_")
        path = os.path.join(self.minecraft_folder, "sokoclient_mods", safe_loader, safe_version)
        os.makedirs(path, exist_ok=True); return path
    def activate(self, version, loader):
        source = self.folder(version, loader); target = os.path.join(self.minecraft_folder, "mods"); os.makedirs(target, exist_ok=True)
        state = os.path.join(target, ".sokoclient-active-mods.json")
        try:
            with open(state, encoding="utf-8") as handle: previous = json.load(handle).get("files", [])
        except (OSError, json.JSONDecodeError): previous = []
        for name in previous:
            path = os.path.join(target, name)
            if os.path.isfile(path): os.remove(path)
        files = [name for name in os.listdir(source) if name.lower().endswith(".jar")]
        for name in files: shutil.copy2(os.path.join(source, name), os.path.join(target, name))
        with open(state, "w", encoding="utf-8") as handle: json.dump({"loader": loader, "version": version, "files": files}, handle)
        return len(files)
