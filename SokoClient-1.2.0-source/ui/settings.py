import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QComboBox, QLineEdit, QFileDialog, QMessageBox
from utils.config import Config
from ui.theme import stylesheet
from updates.updater import Updater


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Config()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)
        title = QLabel("Ustawienia")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        subtitle = QLabel("Kontroluj środowisko gry, wydajność i wygląd launchera.")
        subtitle.setProperty("role", "muted")
        layout.addWidget(title); layout.addWidget(subtitle)
        self.ram = QSpinBox(); self.ram.setRange(1, 64); self.ram.setValue(self.config.get("ram", 4))
        self.java_path = QLineEdit(self.config.get("java_path", "")); self.java_path.setPlaceholderText("Automatycznie pobierana Java Minecraft")
        java_browse = QPushButton("Wybierz plik Java")
        java_browse.clicked.connect(self.select_java)
        self.folder = QLineEdit(self.config.get("minecraft_folder", "")); self.folder.setPlaceholderText("Domyślny folder .minecraft")
        folder_browse = QPushButton("Wybierz folder")
        folder_browse.clicked.connect(self.select_folder)
        self.jvm = QLineEdit(self.config.get("jvm_arguments", "")); self.jvm.setPlaceholderText("np. -XX:+UseG1GC")
        self.width = QSpinBox(); self.width.setRange(640, 7680); self.width.setValue(self.config.get("resolution_width", 1280))
        self.height = QSpinBox(); self.height.setRange(480, 4320); self.height.setValue(self.config.get("resolution_height", 720))
        self.theme = QComboBox(); self.theme.addItems(["Ciemny", "Jasny"]); self.theme.setCurrentText(self.config.get("theme", "Ciemny"))
        self.update_url = QLineEdit(self.config.get("update_manifest_url", "")); self.update_url.setPlaceholderText("Opcjonalny adres manifestu aktualizacji JSON")
        for label, widget in (("RAM (GB)", self.ram), ("Ścieżka Java", self._row(self.java_path, java_browse)), ("Folder Minecraft", self._row(self.folder, folder_browse)), ("Dodatkowe argumenty JVM", self.jvm), ("Rozdzielczość", self._row(self.width, QLabel("×"), self.height)), ("Motyw", self.theme), ("Aktualizacje", self.update_url)):
            layout.addWidget(QLabel(label)); layout.addWidget(widget)
        actions = QHBoxLayout()
        save = QPushButton("Zapisz ustawienia"); save.setProperty("primary", True); save.clicked.connect(self.save_settings)
        logs = QPushButton("Pokaż log"); logs.clicked.connect(self.show_log)
        updates = QPushButton("Sprawdź aktualizacje"); updates.clicked.connect(self.check_updates)
        actions.addWidget(save); actions.addWidget(logs); actions.addWidget(updates); actions.addStretch()
        layout.addLayout(actions); layout.addStretch()

    def _row(self, *widgets):
        row = QWidget(); layout = QHBoxLayout(row); layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets: layout.addWidget(widget)
        return row

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Wybierz folder Minecraft")
        if folder: self.folder.setText(folder)

    def select_java(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz Java", "", "Java (java.exe);;Wszystkie pliki (*)")
        if path: self.java_path.setText(path)

    def save_settings(self):
        self.config.update({"ram": self.ram.value(), "java_path": self.java_path.text().strip(), "minecraft_folder": self.folder.text().strip(), "jvm_arguments": self.jvm.text().strip(), "resolution_width": self.width.value(), "resolution_height": self.height.value(), "theme": self.theme.currentText(), "update_manifest_url": self.update_url.text().strip()})
        self.window().setStyleSheet(stylesheet(self.theme.currentText()))
        QMessageBox.information(self, "Zapisano", "Ustawienia zostały zapisane.")

    def show_log(self):
        path = os.path.abspath("logs/launcher.log")
        if not os.path.exists(path):
            QMessageBox.information(self, "Logi", "Log zostanie utworzony przy następnym uruchomieniu.")
            return
        os.startfile(path)

    def check_updates(self):
        url = self.update_url.text().strip()
        if not url:
            QMessageBox.information(self, "Aktualizacje", "Dodaj adres manifestu aktualizacji w Ustawieniach, aby włączyć automatyczne sprawdzanie.")
            return
        try:
            manifest = Updater(self.config.get("launcher_version", "1.1.0")).check(url)
            version = manifest.get("version") if manifest else None
            if Updater(self.config.get("launcher_version", "1.1.0")).is_newer(version):
                QMessageBox.information(self, "Aktualizacja dostępna", f"Dostępna jest wersja {version}.\n{manifest.get('notes', '')}")
            else:
                QMessageBox.information(self, "Aktualizacje", "Masz aktualną wersję SokoClienta.")
        except Exception as error:
            QMessageBox.warning(self, "Aktualizacje", f"Nie udało się sprawdzić aktualizacji:\n{error}")


