import json
import os
import tempfile


class Config:
    """Small, fault-tolerant persistent settings store for the launcher."""

    def __init__(self, file="config.json"):
        self.file = file
        self.data = {}
        self.load()

    @staticmethod
    def defaults():
        return {
            "username": "", "ram": 4, "java": "Automatycznie", "java_path": "",
            "version": "1.21.4", "loader": "Fabric", "minecraft_folder": "",
            "jvm_arguments": "", "resolution_width": 1280, "resolution_height": 720,
            "theme": "Ciemny", "active_profile": "Domyślny",
            "update_manifest_url": "", "launcher_version": "1.1.0",
        }

    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r", encoding="utf-8") as handle:
                    loaded = json.load(handle)
                if not isinstance(loaded, dict):
                    raise ValueError("Konfiguracja nie jest obiektem JSON")
                self.data = {**self.defaults(), **loaded}
            else:
                self.data = self.defaults()
                self.save()
        except (OSError, json.JSONDecodeError, ValueError):
            self.data = self.defaults()
            self.save()

    def save(self):
        directory = os.path.dirname(os.path.abspath(self.file))
        os.makedirs(directory, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix="config-", suffix=".json", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.data, handle, indent=2, ensure_ascii=False)
            os.replace(temporary, self.file)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def update(self, values):
        self.data.update(values)
        self.save()
