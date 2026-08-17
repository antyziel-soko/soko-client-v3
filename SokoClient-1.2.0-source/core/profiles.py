import json
import os


class ProfileManager:
    """Per-profile launch options, stored independently from global settings."""

    def __init__(self, file="data/profiles.json"):
        self.file = file
        self.profiles = {}
        self.load()

    def load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as handle:
                self.profiles = json.load(handle)
        except (OSError, json.JSONDecodeError):
            self.profiles = {"Domyślny": {"version": "1.21.4", "loader": "Fabric", "ram": 4}}
            self.save()

    def save(self):
        os.makedirs(os.path.dirname(self.file) or ".", exist_ok=True)
        with open(self.file, "w", encoding="utf-8") as handle:
            json.dump(self.profiles, handle, indent=2, ensure_ascii=False)

    def create_profile(self, name, version, loader, ram=4):
        name = name.strip()
        if not name:
            raise ValueError("Profil musi mieć nazwę.")
        if name in self.profiles:
            raise ValueError("Profil o tej nazwie już istnieje.")
        self.profiles[name] = {"version": version, "loader": loader, "ram": int(ram)}
        self.save()

    def update_profile(self, name, **values):
        if name not in self.profiles:
            raise KeyError(name)
        self.profiles[name].update({key: value for key, value in values.items() if value is not None})
        self.save()

    def delete_profile(self, name):
        if name == "Domyślny":
            raise ValueError("Nie można usunąć profilu Domyślny.")
        self.profiles.pop(name, None)
        self.save()

    def get_profiles(self):
        return self.profiles.copy()
