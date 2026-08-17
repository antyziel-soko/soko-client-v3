from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox
)

from mods.search import ModrinthSearch
from mods.install import ModInstaller
from api.modrinth import ModrinthAPI
from services.mod_service import ModService


class ModpackModsDialog(QDialog):

    def __init__(self, parent, modpack_path, minecraft_version, loader):
        super().__init__(parent)

        self.setWindowTitle("Mody w modpacku")
        self.resize(500, 500)

        self.modpack_mods_folder = f"{modpack_path}\\mods" if "\\" in modpack_path else f"{modpack_path}/mods"

        self.minecraft_version = minecraft_version
        self.loader = (loader or "").lower()

        self.search_api = ModrinthSearch()
        self.modrinth_api = ModrinthAPI()
        self.installer = ModInstaller(self.modpack_mods_folder)
        self.mod_service = ModService(self.modpack_mods_folder)

        self.search_results = []

        layout = QVBoxLayout()

        info = QLabel(f"Modpack: {minecraft_version} / {loader}")
        layout.addWidget(info)

        search_layout = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Wyszukaj mod...")

        self.search_button = QPushButton("🔍 Szukaj")

        search_layout.addWidget(self.search)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        self.results_list = QListWidget()
        layout.addWidget(QLabel("Wyniki wyszukiwania:"))
        layout.addWidget(self.results_list)

        self.install_button = QPushButton("⬇ Dodaj do modpacka")
        layout.addWidget(self.install_button)

        self.installed_list = QListWidget()
        layout.addWidget(QLabel("Mody w tym modpacku:"))
        layout.addWidget(self.installed_list)

        self.remove_button = QPushButton("🗑 Usuń z modpacka")
        layout.addWidget(self.remove_button)

        self.status = QLabel("Gotowy")
        layout.addWidget(self.status)

        self.setLayout(layout)

        self.search_button.clicked.connect(self.do_search)
        self.install_button.clicked.connect(self.install_selected)
        self.remove_button.clicked.connect(self.remove_selected)

        self.refresh_installed()

    def refresh_installed(self):

        self.installed_list.clear()

        for name in self.mod_service.get_mods():
            self.installed_list.addItem(name)

    def do_search(self):

        query = self.search.text().strip()

        if not query:
            return

        self.status.setText("Szukam...")

        result = self.search_api.search(
            query,
            self.minecraft_version,
            self.loader
        )

        self.search_results = result.get("hits", []) if result else []

        self.results_list.clear()

        for hit in self.search_results:
            self.results_list.addItem(f"{hit.get('title')} — {hit.get('author')}")

        self.status.setText(f"Znaleziono: {len(self.search_results)}")

    def install_selected(self):

        index = self.results_list.currentRow()

        if index < 0 or index >= len(self.search_results):
            QMessageBox.warning(self, "Brak wyboru", "Zaznacz mod na liście wyników.")
            return

        hit = self.search_results[index]
        project_id = hit.get("project_id") or hit.get("slug")

        self.status.setText("Pobieram informacje o wersji...")

        versions = self.modrinth_api.get_versions(
            project_id,
            self.minecraft_version,
            self.loader
        )

        if not versions:
            QMessageBox.critical(self, "Błąd", "Brak pliku dla wybranej wersji/loadera.")
            self.status.setText("Gotowy")
            return

        files = versions[0].get("files", [])

        if not files:
            QMessageBox.critical(self, "Błąd", "Wersja nie zawiera pliku do pobrania.")
            self.status.setText("Gotowy")
            return

        file_info = files[0]

        self.status.setText("Instaluję...")

        success = self.installer.install(file_info["url"], file_info["filename"])

        if success:
            self.status.setText(f"Dodano: {file_info['filename']}")
            self.refresh_installed()
        else:
            QMessageBox.critical(self, "Błąd", "Nie udało się pobrać pliku moda.")
            self.status.setText("Gotowy")

    def remove_selected(self):

        item = self.installed_list.currentItem()

        if not item:
            QMessageBox.warning(self, "Brak wyboru", "Zaznacz mod na liście zainstalowanych.")
            return

        name = item.text()

        if self.mod_service.remove_mod(name):
            self.status.setText(f"Usunięto: {name}")
            self.refresh_installed()
        else:
            QMessageBox.critical(self, "Błąd", "Nie udało się usunąć pliku.")