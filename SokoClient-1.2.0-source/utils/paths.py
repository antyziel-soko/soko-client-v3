import os


class Paths:

    def __init__(self):

        self.home = os.path.expanduser("~")

        self.minecraft = os.path.join(
            self.home,
            "AppData",
            "Roaming",
            ".minecraft"
        )

        self.mods = os.path.join(
            self.minecraft,
            "mods"
        )

        self.logs = os.path.join(
            self.minecraft,
            "logs"
        )

        self.soko = os.path.join(
            self.home,
            "SokoClient"
        )


    def get_minecraft(self):
        return self.minecraft


    def get_mods(self):
        return self.mods


    def get_logs(self):
        return self.logs


    def get_soko(self):
        return self.soko