import logging
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.app import SokoClientApp
from ui.theme import stylesheet
from utils.config import Config
from utils.logger import setup_logging


def main():
    logger = setup_logging()

    def report_exception(kind, value, trace):
        logger.critical("Nieobsłużony wyjątek", exc_info=(kind, value, trace))
        QMessageBox.critical(None, "Nieoczekiwany błąd", "Wystąpił błąd. Szczegóły zapisano w logs/launcher.log.")

    sys.excepthook = report_exception
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet(Config().get("theme", "Ciemny")))
    window = SokoClientApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
