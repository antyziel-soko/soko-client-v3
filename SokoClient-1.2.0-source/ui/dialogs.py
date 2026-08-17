from PySide6.QtWidgets import QMessageBox


class SokoDialog:

    @staticmethod
    def info(parent, title, message):
        QMessageBox.information(
            parent,
            title,
            message
        )

    @staticmethod
    def warning(parent, title, message):
        QMessageBox.warning(
            parent,
            title,
            message
        )

    @staticmethod
    def error(parent, title, message):
        QMessageBox.critical(
            parent,
            title,
            message
        )