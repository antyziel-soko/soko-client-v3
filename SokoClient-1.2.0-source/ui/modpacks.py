import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
    QInputDialog,
    QFileDialog
)

from modpacks.create import ModpackCreator
from modpacks.export import ModpackExporter
from modpacks.importer import ModpackImporter
from modpacks.install import ModpackInstaller
from modpacks.manager import ModpackManager

from core.minecraft import MinecraftLauncher, get_release_version_ids
from core.install import MinecraftInstaller
from core.java import JavaManager
from core.forge import ForgeInstaller
from core.neoforge import NeoForgeInstaller
from utils.paths import Paths

from ui.modpack_mods_dialog import ModpackModsDialog
from ui.launch_thread import GameLaunchThread


class Modpacks(QWidget):

    def __init__(self, auth):
        super().__init__()

        self.auth = auth
        self.paths = Paths()

        self.modpacks_folder = os.path.join(self.paths.get_soko(), "modpacks")
        self.instances_folder = os.path.join(self.paths.get_soko(), "Modpack Player")

        self.manager = ModpackManager(self.modpacks_folder)
        self.creator = ModpackCreator()
        self.exporter = ModpackExporter()
        self.importer = ModpackImporter()
        self.installer = ModpackInstaller()

        self.launch_thread = None

        layout = QVBoxLayout()

        title = QLabel("📦 Modpacki")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.modpack_list = QListWidget()

        buttons = QHBoxLayout()

        self.create_button = QPushButton("➕ Stwórz")
        self.import_button = QPushButton("📥 Importuj")
        self.export_button = QPushButton("📤 Eksportuj")
        self.mods_button = QPushButton("🧩 Zarządzaj modami")
        self.play_button = QPushButton("▶ Uruchom")

        buttons.addWidget(self.create_button)
        buttons.addWidget(self.import_button)
        buttons.addWidget(self.export_button)
        buttons.addWidget(self.mods_button)
        buttons.addWidget(self.play_button)

        layout.addWidget(title)
        layout.addWidget(QLabel("Wybierz modpack z listy poniżej:"))
        layout.addWidget(self.modpack_list)
        layout.addLayout(buttons)

        self.status = QLabel("Gotowy")
        layout.addWidget(self.status)
        layout.addStretch()

        self.setLayout(layout)

        self.create_button.clicked.connect(self.create_modpack)
        self.import_button.clicked.connect(self.import_modpack)
        self.export_button.clicked.connect(self.export_modpack)
        self.mods_button.clicked.connect(self.manage_mods)
        self.play_button.clicked.connect(self.play_modpack)

        self.refresh_list()

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_list()

    def get_version_choices(self):

        versions = get_release_version_ids()

        if versions:
            return versions[:60]

        return ["1.21.4", "1.21", "1.20.1"]

    def refresh_list(self):

        self.modpack_list.clear()

        for name in self.manager.get_modpacks():
            info = self.manager.get_info(name)
            if info:
                label = f"{name} ({info.get('minecraft_version')}, {info.get('loader')})"
            else:
                label = name
            self.modpack_list.addItem(label)

    def get_selected_name(self):
        item = self.modpack_list.currentItem()
        if not item:
            return None
        return item.text().split(" (")[0]

    def get_instance_folder(self, modpack_name):
        return os.path.join(self.instances_folder, modpack_name)

    def create_modpack(self):

        name, ok = QInputDialog.getText(self, "Nowy modpack", "Nazwa modpacka:")
        if not ok or not name.strip():
            return
        name = name.strip()

        version, ok = QInputDialog.getItem(
            self, "Wersja Minecraft", "Wybierz wersję:",
            self.get_version_choices(), editable=False
        )
        if not ok:
            return

        loader, ok = QInputDialog.getItem(
            self, "Loader", "Wybierz loader:",
            ["Fabric", "Forge", "NeoForge", "Vanilla"], editable=False
        )
        if not ok:
            return

        path = os.path.join(self.modpacks_folder, name)
        self.creator.create(name, version, loader, path)

        self.status.setText(f"Utworzono modpack: {name}")
        self.refresh_list()

    def import_modpack(self):

        zip_file, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik modpacka (.zip)", "", "Archiwa ZIP (*.zip)"
        )
        if not zip_file:
            return

        name = os.path.splitext(os.path.basename(zip_file))[0]
        destination = os.path.join(self.modpacks_folder, name)

        success = self.importer.import_pack(zip_file, destination)

        if success:
            self.status.setText(f"Zaimportowano: {name}")
            self.refresh_list()
        else:
            QMessageBox.critical(self, "Błąd", "Nie udało się zaimportować modpacka.")

    def export_modpack(self):

        name = self.get_selected_name()
        if not name:
            QMessageBox.warning(self, "Brak wyboru", "Zaznacz modpack na liście.")
            return

        folder = os.path.join(self.modpacks_folder, name)

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Zapisz jako", f"{name}.zip", "Archiwa ZIP (*.zip)"
        )
        if not output_file:
            return

        success = self.exporter.export(folder, output_file)

        if success:
            self.status.setText(f"Wyeksportowano do: {output_file}")
        else:
            QMessageBox.critical(self, "Błąd", "Nie udało się wyeksportować modpacka.")

    def manage_mods(self):

        name = self.get_selected_name()

        if not name:
            QMessageBox.warning(self, "Brak wyboru", "Najpierw zaznacz modpack na liście.")
            return

        info = self.manager.get_info(name)

        if not info:
            QMessageBox.critical(self, "Błąd", "Nie znaleziono modpack.json dla tego modpacka.")
            return

        modpack_path = os.path.join(self.modpacks_folder, name)

        dialog = ModpackModsDialog(
            self,
            modpack_path,
            info.get("minecraft_version"),
            info.get("loader")
        )

        dialog.exec()

    def play_modpack(self):

        name = self.get_selected_name()

        if not name:
            QMessageBox.warning(self, "Brak wyboru", "Najpierw zaznacz modpack na liście.")
            return

        account = self.auth.current_account()

        if account is None:
            QMessageBox.warning(self, "Brak konta", "Dodaj konto w zakładce Konto.")
            return

        info = self.manager.get_info(name)

        if not info:
            QMessageBox.critical(self, "Błąd", "Nie znaleziono modpack.json.")
            return

        modpack_path = os.path.join(self.modpacks_folder, name)
        instance_folder = self.get_instance_folder(name)

        launcher = MinecraftLauncher(instance_folder)
        installer = MinecraftInstaller(instance_folder)
        java_manager = JavaManager()
        forge_installer = ForgeInstaller(instance_folder)
        neoforge_installer = NeoForgeInstaller(instance_folder)
        modpack_installer = self.installer

        version = info.get("minecraft_version")
        loader = info.get("loader")
        username = account["username"]
        uuid = account.get("uuid", "") or ""
        access_token = account.get("access_token", "") or ""

        def work(report_status):

            if not launcher.is_installed(version):
                report_status(f"Instaluję Minecraft {version} dla modpacka {name}...")
                installer.install(version)

            report_status("Przygotowuję Javę...")
            java_exe = java_manager.ensure_runtime(instance_folder, version)
            java_bin = java_manager.get_runtime_bin_folder(java_exe)

            if loader == "Fabric":

                if not launcher.is_fabric_installed(version):
                    report_status(f"Instaluję Fabric dla {name}...")
                    launcher.install_fabric(version, java_bin_folder=java_bin)

                run_version_id = launcher.find_fabric_version_id(version)

            elif loader == "Forge":

                if not launcher.is_forge_installed(version):

                    forge_version = forge_installer.find_version(version)

                    if not forge_version:
                        raise Exception(f"Nie znaleziono wersji Forge dla {version}.")

                    report_status(f"Instaluję Forge {forge_version} dla {name}...")
                    forge_installer.install(forge_version, java_bin_folder=java_bin)

                run_version_id = launcher.find_forge_version_id(version)

            elif loader == "NeoForge":

                if not launcher.is_neoforge_installed(version):

                    neoforge_version = neoforge_installer.find_version(version)

                    if not neoforge_version:
                        raise Exception(f"Nie znaleziono wersji NeoForge dla {version}.")

                    report_status(f"Instaluję NeoForge {neoforge_version} dla {name}...")
                    neoforge_installer.install(neoforge_version, java_bin_folder=java_bin)

                run_version_id = launcher.find_neoforge_version_id(version)

            else:

                run_version_id = version

            if not run_version_id:
                raise Exception("Nie udało się ustalić wersji do uruchomienia po instalacji.")

            report_status(f"Wgrywam mody modpacka {name}...")
            modpack_installer.install(modpack_path, instance_folder)

            launcher.launch(run_version_id, username, 4, java_exe, uuid, access_token)

            return f"Uruchomiono modpack: {name} (folder: {instance_folder})"

        self.play_button.setEnabled(False)
        self.status.setText("Startuję...")

        self.launch_thread = GameLaunchThread(work)
        self.launch_thread.status_update.connect(self.status.setText)
        self.launch_thread.finished_success.connect(self.on_launch_success)
        self.launch_thread.finished_error.connect(self.on_launch_error)
        self.launch_thread.start()

    def on_launch_success(self, message):
        self.status.setText(message)
        self.play_button.setEnabled(True)

    def on_launch_error(self, error):
        self.status.setText("Gotowy")
        self.play_button.setEnabled(True)
        QMessageBox.critical(self, "Błąd", error)