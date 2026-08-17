from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.title = QLabel("Soko Client")
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)

        layout.addWidget(self.title)

        self.setLayout(layout)