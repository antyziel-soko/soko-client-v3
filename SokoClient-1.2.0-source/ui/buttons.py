from PySide6.QtWidgets import QPushButton


class SokoButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setMinimumHeight(40)

        self.setStyleSheet("""
            QPushButton {
                background-color: #1f6feb;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #388bfd;
            }

            QPushButton:pressed {
                background-color: #1158c7;
            }
        """)