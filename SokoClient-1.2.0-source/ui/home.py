import logging
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QListWidget,
    QMessageBox,
    QInputDialog,
    QProgressBar,
    QFrame,
    QSlider,
    QFileDialog,
    QSizePolicy,
)
from core.minecraft import MinecraftLauncher, get_release_version_ids
from core.install import MinecraftInstaller
from core.java import JavaManager
from core.forge import ForgeInstaller
from core.neoforge import NeoForgeInstaller
from core.profiles import ProfileManager
from utils.paths import Paths
from utils.config import Config
from ui.launch_thread import GameLaunchThread
from services.mod_library import ModLibrary


class Home(QWidget):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.paths = Paths()
        self.config = Config()
        self.profiles = ProfileManager()
        self.launch_thread = None
        self.logger = logging.getLogger("SokoClient.Home")
        self.launcher = self.installer = self.forge_installer = self.neoforge_installer = None
        self.java_manager = JavaManager()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        self.greeting = QLabel()
        self.greeting.setStyleSheet("font-size: 28px; font-weight: 800;")
        self.intro = QLabel("Dashboard SokoClient — profil, wersja, Java i pamięć RAM w jednym widoku.")
        self.intro.setProperty("role", "muted")

        header = QFrame()
        header.setProperty("card", True)
        header_layout = QHBoxLayout(header)
        header_layout.setSpacing(18)

        left_title = QVBoxLayout()
        left_title.addWidget(self.greeting)
        left_title.addWidget(self.intro)
        left_title.addStretch()

        self.status_recent = QLabel()
        self.status_recent.setProperty("role", "muted")
        self.fps_label = QLabel()
        self.java_status = QLabel()
        self.java_status.setProperty("role", "muted")
        self.mods_status = QLabel()
        self.mods_status.setProperty("role", "muted")

        right_status = QFrame()
        right_status.setProperty("panel", True)
        right_layout = QVBoxLayout(right_status)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(10)
        right_layout.addWidget(QLabel("Szybki podgląd"))
        right_layout.addWidget(self.status_recent)
        right_layout.addWidget(self.fps_label)
        right_layout.addWidget(self.java_status)
        right_layout.addWidget(self.mods_status)
        right_layout.addStretch()

        header_layout.addLayout(left_title, 2)
        header_layout.addWidget(right_status, 1)

        layout.addWidget(header)

        body = QHBoxLayout()
        body.setSpacing(18)

        profile_card = QFrame()
        profile_card.setProperty("card", True)
        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(20, 18, 20, 18)
        profile_layout.setSpacing(12)
        profile_layout.addWidget(QLabel("Profile"))

        self.profile_list = QListWidget()
        self.profile_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.profile_list.setSelectionMode(QListWidget.SingleSelection)
        profile_layout.addWidget(self.profile_list)

        profile_buttons = QHBoxLayout()
        self.new_profile = QPushButton("Nowy profil")
        self.new_profile.setProperty("small", True)
        self.delete_profile = QPushButton("Usuń profil")
        self.delete_profile.setProperty("small", True)
        profile_buttons.addWidget(self.new_profile)
        profile_buttons.addWidget(self.delete_profile)
        profile_layout.addLayout(profile_buttons)

        profile_layout.addStretch()

        launch_card = QFrame()
        launch_card.setProperty("card", True)
        launch_layout = QVBoxLayout(launch_card)
        launch_layout.setContentsMargins(20, 18, 20, 18)
        launch_layout.setSpacing(14)
        launch_layout.addWidget(QLabel("Uruchom Minecraft"))

        version_row = QHBoxLayout()
        version_row.addWidget(QLabel("Wersja"))
        self.version = QComboBox()
        version_row.addWidget(self.version, 1)
        loader_row = QHBoxLayout()
        loader_row.addWidget(QLabel("Loader"))
        self.loader = QComboBox()
        self.loader.addItems(["Fabric", "Forge", "NeoForge", "Vanilla"])
        loader_row.addWidget(self.loader, 1)

        ram_label = QLabel("RAM")
        self.ram_slider = QSlider(Qt.Horizontal)
        self.ram_slider.setRange(2, 16)
        self.ram_slider.setTickInterval(1)
        self.ram_slider.setTickPosition(QSlider.TicksBelow)
        self.ram_slider.setSingleStep(1)
        self.ram_value = QLabel()
        self.ram_value.setFixedWidth(70)

        ram_row = QHBoxLayout()
        ram_row.addWidget(ram_label)
        ram_row.addWidget(self.ram_slider, 1)
        ram_row.addWidget(self.ram_value)

        self.java_change_button = QPushButton("Zmień Java")
        self.java_change_button.setProperty("small", True)

        self.play_button = QPushButton("GRAJ")
        self.play_button.setProperty("primary", True)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.status = QLabel("Gotowy")
        self.status.setProperty("role", "muted")

        launch_layout.addLayout(version_row)
        launch_layout.addLayout(loader_row)
        launch_layout.addLayout(ram_row)
        launch_layout.addWidget(self.java_change_button)
        launch_layout.addWidget(self.play_button)
        launch_layout.addWidget(self.progress)
        launch_layout.addWidget(self.status)

        body.addWidget(profile_card, 1)
        body.addWidget(launch_card, 2)

        layout.addLayout(body)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(18)

        installed_card = QFrame()
        installed_card.setProperty("card", True)
        installed_layout = QVBoxLayout(installed_card)
        installed_layout.setContentsMargins(20, 18, 20, 18)
        installed_layout.setSpacing(10)
        installed_layout.addWidget(QLabel("Zainstalowane wersje"))
        self.installed = QListWidget()
        self.installed.setMaximumHeight(180)
        installed_layout.addWidget(self.installed)

        mods_card = QFrame()
        mods_card.setProperty("card", True)
        mods_layout = QVBoxLayout(mods_card)
        mods_layout.setContentsMargins(20, 18, 20, 18)
        mods_layout.setSpacing(10)
        mods_layout.addWidget(QLabel("Mody w bieżącym zestawie"))
        self.mods_list = QListWidget()
        self.mods_list.setMaximumHeight(180)
        mods_layout.addWidget(self.mods_list)

        bottom_row.addWidget(installed_card, 1)
        bottom_row.addWidget(mods_card, 1)
        layout.addLayout(bottom_row)

        self.profile_list.itemClicked.connect(self.on_profile_selected)
        self.new_profile.clicked.connect(self.create_profile)
        self.delete_profile.clicked.connect(self.remove_profile)
        self.ram_slider.valueChanged.connect(self.update_ram_label)
        self.java_change_button.clicked.connect(self.select_java)
        self.play_button.clicked.connect(self.start_game)
        self.loader.currentTextChanged.connect(self.save_loader_version)
        self.version.currentTextChanged.connect(self.save_loader_version)

        self.populate_versions()
        self.refresh_profiles()
        self.update_ram_label(self.config.get("ram", 8))
        self.refresh_dashboard()

    def get_minecraft_folder(self):
        return self.config.get("minecraft_folder") or self.paths.get_minecraft()

    def populate_versions(self):
        versions = get_release_version_ids() or ["1.21.4", "1.21", "1.20.1"]
        self.version.clear()
        self.version.addItems(versions[:60])

    def refresh_profiles(self):
        active = self.config.get("active_profile", "Domyślny")
        profiles = self.profiles.get_profiles()

        self.profile_list.clear()
        for name, data in profiles.items():
            self.profile_list.addItem(f"{name} — {data.get('version')} {data.get('loader')} / {data.get('ram')}GB")

        for index in range(self.profile_list.count()):
            item = self.profile_list.item(index)
            if item.text().startswith(active + " "):
                self.profile_list.setCurrentItem(item)
                break

        self.load_profile(active)

    def load_profile(self, name):
        data = self.profiles.get_profiles().get(name, {})
        self.version.setCurrentText(data.get("version", self.config.get("version", "1.21.4")))
        self.loader.setCurrentText(data.get("loader", self.config.get("loader", "Fabric")))
        current_ram = int(data.get("ram", self.config.get("ram", 8)))
        self.ram_slider.setValue(current_ram)
        self.config.set("active_profile", name)
        self.refresh_dashboard()

    def on_profile_selected(self, item):
        name = item.text().split(" — ")[0]
        self.load_profile(name)

    def create_profile(self):
        name, ok = QInputDialog.getText(self, "Nowy profil", "Nazwa profilu:")
        if not ok or not name.strip():
            return
        try:
            self.profiles.create_profile(
                name,
                self.version.currentText(),
                self.loader.currentText(),
                self.ram_slider.value(),
            )
            self.refresh_profiles()
        except ValueError as error:
            QMessageBox.warning(self, "Profil", str(error))

    def remove_profile(self):
        current = self.config.get("active_profile", "Domyślny")
        try:
            self.profiles.delete_profile(current)
            self.refresh_profiles()
        except ValueError as error:
            QMessageBox.warning(self, "Profil", str(error))

    def save_loader_version(self):
        self.config.update({
            "version": self.version.currentText(),
            "loader": self.loader.currentText(),
        })

    def refresh_dashboard(self):
        account = self.auth.current_account()
        username = account["username"] if account else "Gracz"
        self.greeting.setText(f"Witaj, {username}")

        last_run = self.config.get("last_launched")
        self.status_recent.setText(f"Ostatnio uruchomiono: {last_run}" if last_run else "Wybierz profil i kliknij GRAJ.")
        self.fps_label.setText("FPS: N/A")

        java_candidates = self.java_manager.detect_javas()
        configured = self.config.get("java_path", "")
        java_lines = []
        if configured:
            java_lines.append(f"Wybrana Java: {configured}")
        for version in (21, 17, 8):
            java_lines.append(f"{'✓' if version in java_candidates else '✗'} Java {version}")
        self.java_status.setText(" • ".join(java_lines))

        mods = self.get_mods()
        self.mods_status.setText(f"Mody: {len(mods)} w aktywnym zestawie {self.loader.currentText()} {self.version.currentText()}")

        self.refresh_account()
        self.refresh_installed()
        self.refresh_mod_list()

    def update_ram_label(self, value):
        self.ram_value.setText(f"{value} GB")
        self.config.set("ram", value)

    def select_java(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik Java", "", "Java executable (java.exe);;Wszystkie pliki (*)")
        if not path:
            return
        self.config.set("java_path", path)
        self.refresh_dashboard()

    def refresh_account(self):
        account = self.auth.current_account()
        if account:
            self.status_recent.setText(f"Aktywne konto: {account['username']}")
        else:
            self.status_recent.setText("Aktywne konto: brak — dodaj je w zakładce Konto")

    def refresh_installed(self):
        folder = self.get_minecraft_folder()
        os_launcher = MinecraftLauncher(folder)
        versions = os_launcher.get_installed_versions() or ["Brak zainstalowanych wersji"]
        self.installed.clear()
        self.installed.addItems(versions)

    def get_mods(self):
        folder = self.get_minecraft_folder()
        library = ModLibrary(folder)
        version = self.version.currentText()
        loader = self.loader.currentText()
        mods_folder = library.folder(version, loader)
        if not os.path.isdir(mods_folder):
            return []
        return [name for name in os.listdir(mods_folder) if name.lower().endswith(".jar")]

    def refresh_mod_list(self):
        mods = self.get_mods()
        self.mods_list.clear()
        if not mods:
            self.mods_list.addItem("Brak modów w aktywnym zestawie")
            return
        self.mods_list.addItems(sorted(mods))

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_dashboard()

    def start_game(self):
        account = self.auth.current_account()
        if not account:
            QMessageBox.warning(self, "Brak konta", "Dodaj konto w zakładce Konto.")
            return

        active = self.config.get("active_profile", "Domyślny")
        version = self.version.currentText()
        loader = self.loader.currentText()
        ram = self.ram_slider.value()
        folder = self.get_minecraft_folder()

        self.profiles.update_profile(active, version=version, loader=loader, ram=ram)
        self.config.set("last_launched", f"{version} {loader}")

        launcher = MinecraftLauncher(folder)
        installer = MinecraftInstaller(folder)
        forge = ForgeInstaller(folder)
        neoforge = NeoForgeInstaller(folder)

        def work(report):
            report("Sprawdzam pliki gry…")
            if not launcher.is_installed(version):
                report(f"Pobieram Minecraft {version}…")
                installer.install(version)

            configured_java = self.config.get("java_path", "")
            if configured_java:
                if not os.path.isfile(configured_java):
                    raise RuntimeError("Wybrana ścieżka Java nie istnieje. Popraw ją w Ustawieniach.")
                java_exe = configured_java
            else:
                report("Przygotowuję Javę…")
                java_exe = self.java_manager.ensure_runtime(folder, version)

            java_bin = self.java_manager.get_runtime_bin_folder(java_exe)

            if loader == "Fabric":
                if not launcher.is_fabric_installed(version):
                    report("Instaluję Fabric…")
                    launcher.install_fabric(version, java_bin_folder=java_bin)
                run_id = launcher.find_fabric_version_id(version)
            elif loader == "Forge":
                if not launcher.is_forge_installed(version):
                    forge_version = forge.find_version(version)
                    if not forge_version:
                        raise RuntimeError(f"Nie znaleziono Forge dla {version}.")
                    report(f"Instaluję Forge {forge_version}…")
                    forge.install(forge_version, java_bin_folder=java_bin)
                run_id = launcher.find_forge_version_id(version)
            elif loader == "NeoForge":
                if not launcher.is_neoforge_installed(version):
                    neo_version = neoforge.find_version(version)
                    if not neo_version:
                        raise RuntimeError(f"Nie znaleziono NeoForge dla {version}.")
                    report(f"Instaluję NeoForge {neo_version}…")
                    neoforge.install(neo_version, java_bin_folder=java_bin)
                run_id = launcher.find_neoforge_version_id(version)
            else:
                run_id = version

            if not run_id:
                raise RuntimeError("Instalacja loadera nie utworzyła wersji do uruchomienia.")

            count = ModLibrary(folder).activate(version, loader)
            report(f"Aktywuję {count} modów dla {loader} {version}…")
            report("Uruchamiam Minecraft…")
            launcher.launch(
                run_id,
                account["username"],
                ram,
                java_exe,
                account.get("uuid", ""),
                account.get("access_token", ""),
                self.config.get("jvm_arguments", ""),
                (
                    self.config.get("resolution_width", 1280),
                    self.config.get("resolution_height", 720),
                ),
            )
            return f"Uruchomiono {version} ({loader}) jako {account['username']}"

        self.play_button.setEnabled(False)
        self.progress.setRange(0, 0)
        self.status.setText("Startuję…")

        self.launch_thread = GameLaunchThread(work)
        self.launch_thread.status_update.connect(self.status.setText)
        self.launch_thread.finished_success.connect(self.on_launch_success)
        self.launch_thread.finished_error.connect(self.on_launch_error)
        self.launch_thread.start()

    def on_launch_success(self, message):
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.status.setText(message)
        self.play_button.setEnabled(True)
        self.refresh_installed()
        self.refresh_mod_list()

    def on_launch_error(self, error):
        self.logger.exception("Błąd uruchamiania: %s", error)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.status.setText("Nie udało się uruchomić gry")
        self.play_button.setEnabled(True)
        QMessageBox.critical(self, "Błąd uruchamiania", f"{error}\n\nSzczegóły: logs/launcher.log")

