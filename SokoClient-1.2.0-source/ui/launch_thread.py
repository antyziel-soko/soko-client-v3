from PySide6.QtCore import QThread, Signal


class GameLaunchThread(QThread):

    status_update = Signal(str)
    finished_success = Signal(str)
    finished_error = Signal(str)

    def __init__(self, work_function):
        super().__init__()
        self.work_function = work_function

    def run(self):
        try:
            result = self.work_function(self.report_status)
            self.finished_success.emit(result or "")
        except Exception as e:
            self.finished_error.emit(str(e))

    def report_status(self, text):
        self.status_update.emit(text)