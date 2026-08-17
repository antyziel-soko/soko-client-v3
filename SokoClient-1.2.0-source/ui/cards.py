from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class ModCard(QFrame):
    def __init__(self, name, description=""):
        super().__init__()

        layout = QVBoxLayout()

        self.name = QLabel(name)
        self.name.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.description = QLabel(description)

        self.install_button = QPushButton("⬇ Instaluj")

        layout.addWidget(self.name)
        layout.addWidget(self.description)
        layout.addWidget(self.install_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QFrame {
                background-color: #17171c;
                border-radius: 15px;
                padding: 10px;
            }
        """)