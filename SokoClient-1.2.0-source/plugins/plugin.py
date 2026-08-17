import os
import importlib.util


class PluginManager:

    def __init__(self, plugins_folder="plugins"):
        self.plugins_folder = plugins_folder
        self.plugins = []

    def load_plugins(self):

        if not os.path.exists(self.plugins_folder):
            return

        for file in os.listdir(self.plugins_folder):

            if not file.endswith(".py"):
                continue

            if file == "plugin.py":
                continue

            path = os.path.join(
                self.plugins_folder,
                file
            )

            name = os.path.splitext(file)[0]

            spec = importlib.util.spec_from_file_location(
                name,
                path
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.plugins.append(module)

    def get_plugins(self):
        return self.plugins