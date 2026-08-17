import json
import os


class Cache:

    def __init__(self, file="data/cache.json"):
        self.file = file
        self.data = {}

        self.load()


    def load(self):

        if os.path.exists(self.file):

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:
                self.data = json.load(f)

        else:
            self.data = {}
            self.save()


    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4
            )


    def set(self, key, value):

        self.data[key] = value
        self.save()


    def get(self, key):

        return self.data.get(key)


    def clear(self):

        self.data = {}
        self.save()