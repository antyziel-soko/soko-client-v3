import webbrowser

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication


class TopBar(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(50)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)

        layout.addStretch()

        # TikTok - link
        tiktok_button = QPushButton("🎵 TikTok")
        tiktok_button.setMinimumHeight(35)
        tiktok_button.clicked.connect(
            lambda: webbrowser.open(
                "https://www.tiktok.com/@sokowir0wka_antek?_r=1&_t=ZN-983tultu5FG"
            )
        )
        layout.addWidget(tiktok_button)

        # YouTube - link
        youtube_button = QPushButton("▶ YouTube")
        youtube_button.setMinimumHeight(35)
        youtube_button.clicked.connect(
            lambda: webbrowser.open(
                "https://www.youtube.com/@sokowir%C3%B3wka_antek"
            )
        )
        layout.addWidget(youtube_button)

        # Discord - tylko tag (brak linku z zaproszeniem), klik = kopiuje do schowka
        self.discord_tag = "antekker_01646"

        discord_button = QPushButton(f"💬 {self.discord_tag}")
        discord_button.setMinimumHeight(35)
        discord_button.setToolTip("Kliknij, aby skopiować tag Discord")
        discord_button.clicked.connect(self.copy_discord_tag)
        layout.addWidget(discord_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #17171c;
                border-bottom: 1px solid #24242b;
            }

            QPushButton {
                background-color: #24242b;
                color: white;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #1f6feb;
            }
        """)

    def copy_discord_tag(self):
        QApplication.clipboard().setText(self.discord_tag)