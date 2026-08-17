import subprocess


class LauncherService:

    def __init__(self):
        self.process = None


    def launch(self, command):

        try:
            self.process = subprocess.Popen(
                command,
                shell=True
            )

            return True

        except Exception:
            return False


    def stop(self):

        if self.process:
            self.process.terminate()
            return True

        return False