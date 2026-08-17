import json
import os


class Storage:

    def __init__(self, folder="storage"):
        self.folder = folder

        os.makedirs(
            self.folder,
            exist_ok=True
        )


    def save(self, name, data):

        path = os.path.join(
            self.folder,
            f"{name}.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )


    def load(self, name):

        path = os.path.join(
            self.folder,
            f"{name}.json"
        )

        if not os.path.exists(path):
            return None

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

        if not content:
            return None

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None


    def delete(self, name):

        path = os.path.join(
            self.folder,
            f"{name}.json"
        )

        if os.path.exists(path):
            os.remove(path)
            return True

        return False


    def exists(self, name):

        return os.path.exists(
            os.path.join(
                self.folder,
                f"{name}.json"
            )
        )