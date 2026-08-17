import webbrowser

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QInputDialog,
    QApplication
)

from utils.config import Config
from core.microsoft_auth import MicrosoftAuth


class Account(QWidget):

    def __init__(self, auth):
        super().__init__()

        self.auth = auth
        self.config = Config()

        layout = QVBoxLayout()

        title = QLabel("👤 Konto")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.accounts = QListWidget()

        login_layout = QHBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Nazwa gracza (offline)...")

        self.login_button = QPushButton("🔑 Dodaj konto offline")

        login_layout.addWidget(self.username)
        login_layout.addWidget(self.login_button)

        self.premium_button = QPushButton("🪟 Zaloguj przez Microsoft (premium)")

        self.select_button = QPushButton("✅ Ustaw jako aktywne")
        self.logout_button = QPushButton("🚪 Usuń konto")

        layout.addWidget(title)
        layout.addWidget(QLabel("Konta:"))
        layout.addWidget(self.accounts)
        layout.addLayout(login_layout)
        layout.addWidget(self.premium_button)
        layout.addWidget(self.select_button)
        layout.addWidget(self.logout_button)

        self.status = QLabel("Gotowy")
        layout.addWidget(self.status)

        layout.addStretch()

        self.setLayout(layout)

        self.login_button.clicked.connect(self.add_account)
        self.logout_button.clicked.connect(self.remove_account)
        self.select_button.clicked.connect(self.select_account)
        self.premium_button.clicked.connect(self.login_premium)

        self.refresh_list()

    def refresh_list(self):

        self.accounts.clear()

        current = self.auth.current_account()
        current_name = current["username"] if current else None

        for account in self.auth.get_accounts_full():

            name = account.get("username")
            kind = "premium" if account.get("type") == "premium" else "offline"

            label = f"{name} [{kind}]"

            if name == current_name:
                label += " (aktywne)"

            self.accounts.addItem(label)

    def add_account(self):

        name = self.username.text().strip()

        if name:
            self.auth.login(name)
            self.username.clear()
            self.refresh_list()

    def remove_account(self):

        item = self.accounts.currentItem()

        if item:
            name = item.text().split(" [")[0]
            self.auth.logout(name)
            self.refresh_list()

    def select_account(self):

        item = self.accounts.currentItem()

        if item:
            name = item.text().split(" [")[0]
            self.auth.set_current_account(name)
            self.refresh_list()

    def login_premium(self):

        client_id = self.config.get("ms_client_id") or None

        ms_auth = MicrosoftAuth(client_id)

        try:
            url, state, code_verifier = ms_auth.get_login_url()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))
            return

        webbrowser.open(url)

        redirect_url, ok = QInputDialog.getText(
            self,
            "Logowanie Microsoft",
            "1) Zaloguj się w otwartej przeglądarce swoim kontem Microsoft.\n"
            "2) Po zalogowaniu strona będzie pusta/pokaże błąd - to normalne.\n"
            "3) Skopiuj CAŁY adres z paska adresu przeglądarki i wklej go poniżej:"
        )

        if not ok or not redirect_url.strip():
            return

        self.status.setText("Loguję...")
        QApplication.processEvents()

        try:
            account_info = ms_auth.complete_login(redirect_url.strip(), code_verifier)
        except Exception as e:
            self.status.setText("Gotowy")
            QMessageBox.critical(self, "Błąd logowania", str(e))
            return

        username = account_info.get("name")
        uuid = account_info.get("id")
        access_token = account_info.get("access_token")
        refresh_token = account_info.get("refresh_token")

        self.auth.login_premium(username, uuid, access_token, refresh_token)

        self.status.setText(f"Zalogowano jako {username} (premium)")
        self.refresh_list()