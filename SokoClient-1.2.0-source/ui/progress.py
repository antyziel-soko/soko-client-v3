from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)


class DownloadProgress(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.status = QLabel("Gotowy")

        self.progress = QProgressBar()
        self.progress.setValue(0)

        layout.addWidget(self.status)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def update_progress(self, value, text="Pobieranie..."):
        self.progress.setValue(value)
        self.status.setText(text)