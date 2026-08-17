from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QHBoxLayout, QMessageBox
from mods.search import ModrinthSearch
from mods.install import ModInstaller
from api.modrinth import ModrinthAPI
from services.mod_service import ModService
from services.mod_library import ModLibrary
from utils.config import Config
from utils.paths import Paths


class Mods(QWidget):
    def __init__(self):
        super().__init__()
        self.paths, self.config = Paths(), Config(); self.search_api, self.modrinth_api = ModrinthSearch(), ModrinthAPI(); self.search_results = []
        layout = QVBoxLayout(self); layout.setContentsMargins(32, 28, 32, 28); layout.setSpacing(12)
        title = QLabel("Biblioteka modów"); title.setStyleSheet("font-size: 28px; font-weight: 700;")
        self.location = QLabel(); self.location.setProperty("role", "muted")
        filters = QHBoxLayout(); self.version = QComboBox(); self.version.addItems(["1.21.4", "1.21", "1.20.1"]); self.loader = QComboBox(); self.loader.addItems(["Fabric", "Forge", "NeoForge"])
        filters.addWidget(QLabel("Wersja")); filters.addWidget(self.version); filters.addWidget(QLabel("Loader")); filters.addWidget(self.loader); filters.addStretch()
        self.search = QLineEdit(); self.search.setPlaceholderText("Wyszukaj mod na Modrinth…"); self.search_button = QPushButton("Szukaj")
        search_row = QHBoxLayout(); search_row.addWidget(self.search, 1); search_row.addWidget(self.search_button)
        self.mods_list = QListWidget(); self.install_button = QPushButton("Zainstaluj zaznaczony mod")
        self.installed_list = QListWidget(); self.remove_button = QPushButton("Usuń zaznaczony mod"); self.status = QLabel("Gotowy"); self.status.setProperty("role", "muted")
        for widget in (title, self.location): layout.addWidget(widget)
        layout.addLayout(filters); layout.addLayout(search_row); layout.addWidget(QLabel("Wyniki wyszukiwania")); layout.addWidget(self.mods_list); layout.addWidget(self.install_button); layout.addWidget(QLabel("Mody w wybranym zestawie")); layout.addWidget(self.installed_list); layout.addWidget(self.remove_button); layout.addWidget(self.status)
        self.search_button.clicked.connect(self.do_search); self.install_button.clicked.connect(self.install_selected); self.remove_button.clicked.connect(self.remove_selected); self.version.currentTextChanged.connect(self.refresh_installed); self.loader.currentTextChanged.connect(self.refresh_installed)
        self.version.setCurrentText(self.config.get("version", "1.21.4")); self.loader.setCurrentText(self.config.get("loader", "Fabric")); self.refresh_installed()

    def library_folder(self):
        folder = self.config.get("minecraft_folder") or self.paths.get_minecraft()
        return ModLibrary(folder).folder(self.version.currentText(), self.loader.currentText())
    def refresh_installed(self, *args):
        folder = self.library_folder(); self.location.setText(f"Osobny zestaw: {folder}"); self.installer = ModInstaller(folder); self.mod_service = ModService(folder); self.installed_list.clear(); self.installed_list.addItems(self.mod_service.get_mods())
    def showEvent(self, event): super().showEvent(event); self.refresh_installed()
    def do_search(self):
        query = self.search.text().strip()
        if not query: return
        self.status.setText("Szukam…")
        try: result = self.search_api.search(query, self.version.currentText(), self.loader.currentText().lower())
        except Exception as error: QMessageBox.warning(self, "Mody", f"Nie udało się wyszukać modów:\n{error}"); self.status.setText("Gotowy"); return
        self.search_results = result.get("hits", []) if result else []; self.mods_list.clear()
        for hit in self.search_results: self.mods_list.addItem(f"{hit.get('title', 'Bez nazwy')} — {hit.get('author', 'nieznany autor')}")
        self.status.setText(f"Znaleziono: {len(self.search_results)}")
    def install_selected(self):
        index = self.mods_list.currentRow()
        if not 0 <= index < len(self.search_results): QMessageBox.warning(self, "Brak wyboru", "Zaznacz mod na liście wyników."); return
        self.status.setText("Pobieram informacje o wersji…")
        try: versions = self.modrinth_api.get_versions(self.search_results[index].get("project_id") or self.search_results[index].get("slug"), self.version.currentText(), self.loader.currentText().lower())
        except Exception as error: QMessageBox.warning(self, "Mody", str(error)); return
        if not versions or not versions[0].get("files"): QMessageBox.warning(self, "Brak pliku", "Nie ma pliku dla wybranej wersji i loadera."); self.status.setText("Gotowy"); return
        info = versions[0]["files"][0]
        if self.installer.install(info["url"], info["filename"]): self.status.setText(f"Zainstalowano: {info['filename']}"); self.refresh_installed()
        else: QMessageBox.critical(self, "Błąd", "Nie udało się pobrać pliku moda.")
    def remove_selected(self):
        item = self.installed_list.currentItem()
        if not item: QMessageBox.warning(self, "Brak wyboru", "Zaznacz mod do usunięcia."); return
        if self.mod_service.remove_mod(item.text()): self.status.setText(f"Usunięto: {item.text()}"); self.refresh_installed()
