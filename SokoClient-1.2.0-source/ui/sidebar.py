from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.play_button = QPushButton("🎮 Graj")
        self.mods_button = QPushButton("🧩 Mody")
        self.modpacks_button = QPushButton("📦 Modpacki")
        self.settings_button = QPushButton("⚙️ Ustawienia")
        self.account_button = QPushButton("👤 Konto")

        buttons = [
            self.play_button,
            self.mods_button,
            self.modpacks_button,
            self.settings_button,
            self.account_button
        ]

        for button in buttons:
            button.setMinimumHeight(48)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet("text-align: left;")
            layout.addWidget(button)

        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #141a24;
            }
            QPushButton {
                background-color: #1f2435;
                color: white;
                border-radius: 14px;
                padding: 12px 16px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #2b4f9f;
            }
            QPushButton[active="true"] {
                background-color: #4964d0;
                color: white;
            }
        """)

    def set_active(self, active_button):
        for button in (
            self.play_button,
            self.mods_button,
            self.modpacks_button,
            self.settings_button,
            self.account_button,
        ):
            button.setProperty("active", button is active_button)
            button.style().unpolish(button)
            button.style().polish(button)
