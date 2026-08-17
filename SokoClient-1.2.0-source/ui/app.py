from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QGraphicsOpacityEffect
from core.auth import AuthManager
from ui.topbar import TopBar
from ui.sidebar import Sidebar
from ui.home import Home
from ui.mods import Mods
from ui.modpacks import Modpacks
from ui.settings import Settings
from ui.account import Account


class SokoClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SokoClient")
        self.resize(1280, 820)
        self.auth = AuthManager()
        container = QWidget()
        self.setCentralWidget(container)
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(TopBar())
        body = QWidget()
        layout = QHBoxLayout(body)
        layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)
        self.pages = QStackedWidget()
        self.home = Home(self.auth)
        self.mods = Mods()
        self.modpacks = Modpacks(self.auth)
        self.settings = Settings()
        self.account = Account(self.auth)
        for page in (self.home, self.mods, self.modpacks, self.settings, self.account):
            self.pages.addWidget(page)
        layout.addWidget(self.pages, 1)
        outer.addWidget(body, 1)

        self.sidebar.play_button.clicked.connect(lambda: self.switch_page(self.sidebar.play_button, self.home))
        self.sidebar.mods_button.clicked.connect(lambda: self.switch_page(self.sidebar.mods_button, self.mods))
        self.sidebar.modpacks_button.clicked.connect(lambda: self.switch_page(self.sidebar.modpacks_button, self.modpacks))
        self.sidebar.settings_button.clicked.connect(lambda: self.switch_page(self.sidebar.settings_button, self.settings))
        self.sidebar.account_button.clicked.connect(lambda: self.switch_page(self.sidebar.account_button, self.account))

        self.sidebar.set_active(self.sidebar.play_button)

    def switch_page(self, button, page):
        self.sidebar.set_active(button)
        self.show_page(page)

    def show_page(self, page):
        if self.pages.currentWidget() is page:
            return
        self.pages.setCurrentWidget(page)
        effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", page)
        animation.setDuration(180)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.finished.connect(lambda: page.setGraphicsEffect(None))
        page._transition = animation
        animation.start()
