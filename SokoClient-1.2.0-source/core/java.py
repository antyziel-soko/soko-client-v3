import json
import os
import re
import shutil
import subprocess
import minecraft_launcher_lib


class JavaManager:

    def __init__(self):
        self.java_path = None

    def find_java(self):
        java = shutil.which("java")

        if java:
            self.java_path = java
            return java

        return None

    def check_version(self):
        if not self.java_path:
            self.find_java()

        return bool(self.java_path)

    def get_path(self):
        return self.java_path

    def detect_javas(self):
        runtimes = {}
        candidates = set()

        if os.name == "nt":
            candidates.add(shutil.which("java"))
            java_home = os.environ.get("JAVA_HOME")
            if java_home:
                candidates.add(os.path.join(java_home, "bin", "java.exe"))
        else:
            candidates.add(shutil.which("java"))
            java_home = os.environ.get("JAVA_HOME")
            if java_home:
                candidates.add(os.path.join(java_home, "bin", "java"))

        for candidate in [path for path in candidates if path]:
            version = self._query_version(candidate)
            if version:
                runtimes[version] = candidate

        return runtimes

    def _query_version(self, java_exe):
        try:
            result = subprocess.run(
                [java_exe, "-version"],
                capture_output=True,
                text=True
            )

            output = result.stderr or result.stdout
            if result.returncode != 0 or not output:
                return None

            match = re.search(r'version "(?P<major>\d+)(?:\.(?P<minor>\d+))?', output)
            if not match:
                return None

            major = int(match.group("major"))
            if major == 1:
                minor = int(match.group("minor") or 0)
                return minor

            return major
        except Exception:
            return None

    # ----------------------------
    # Prywatny Java runtime (bez instalacji systemowej)
    # ----------------------------

    def get_required_component(self, minecraft_directory, version_id):

        version_json = os.path.join(
            minecraft_directory,
            "versions",
            version_id,
            f"{version_id}.json"
        )

        component = "java-runtime-gamma"

        if os.path.exists(version_json):

            try:
                with open(version_json, "r", encoding="utf-8") as f:
                    data = json.load(f)

                java_info = data.get("javaVersion")

                if java_info and "component" in java_info:
                    component = java_info["component"]

            except Exception:
                pass

        return component

    def ensure_runtime(self, minecraft_directory, version_id):

        component = self.get_required_component(
            minecraft_directory,
            version_id
        )

        installed = minecraft_launcher_lib.runtime.get_installed_jvm_runtimes(
            minecraft_directory
        )

        if component not in installed:
            minecraft_launcher_lib.runtime.install_jvm_runtime(
                component,
                minecraft_directory
            )

        exe_path = minecraft_launcher_lib.runtime.get_executable_path(
            component,
            minecraft_directory
        )

        if exe_path:
            self.java_path = exe_path

        return exe_path

    def get_runtime_bin_folder(self, exe_path):

        if not exe_path:
            return None

        return os.path.dirname(exe_path)