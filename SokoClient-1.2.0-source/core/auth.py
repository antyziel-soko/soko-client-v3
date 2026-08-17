from core.accounts import AccountManager


class AuthManager:

    def __init__(self):
        self.account_manager = AccountManager()

    def login(self, username):
        if not username:
            return False

        self.account_manager.add_offline_account(username)

        return True

    def login_premium(self, username, uuid, access_token, refresh_token=None):

        self.account_manager.add_premium_account(
            username,
            uuid,
            access_token,
            refresh_token
        )

        return True

    def logout(self, username):
        self.account_manager.remove_account(username)

    def get_logged_accounts(self):
        return [a["username"] for a in self.account_manager.get_accounts()]

    def get_accounts_full(self):
        return self.account_manager.get_accounts()

    def current_account(self):
        return self.account_manager.get_current()

    def set_current_account(self, username):
        self.account_manager.set_current(username)