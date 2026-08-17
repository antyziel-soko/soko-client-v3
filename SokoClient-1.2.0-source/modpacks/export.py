import os
import zipfile


class ModpackExporter:

    def export(self, folder, output_file):

        if not os.path.exists(folder):
            return False

        with zipfile.ZipFile(
            output_file,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for root, dirs, files in os.walk(folder):
                for file in files:

                    path = os.path.join(
                        root,
                        file
                    )

                    zip_file.write(
                        path,
                        os.path.relpath(
                            path,
                            folder
                        )
                    )

        return True