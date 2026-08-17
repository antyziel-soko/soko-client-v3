import os


class SecurityScanner:

    def __init__(self):
        self.suspicious = [
            "meteor",
            "wurst",
            "liquidbounce",
            "thunderhack",
            "catlean",
            "killaura",
            "reach"
        ]


    def scan_folder(self, folder):

        found = []

        if not os.path.exists(folder):
            return found

        for root, dirs, files in os.walk(folder):

            for file in files:

                name = file.lower()

                for word in self.suspicious:

                    if word in name:
                        found.append(
                            os.path.join(
                                root,
                                file
                            )
                        )

        return found