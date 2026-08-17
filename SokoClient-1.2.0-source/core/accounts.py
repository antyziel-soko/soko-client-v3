from security.secure_storage import SecureAccountStorage
from storage.storage import Storage


class AccountManager:
    def __init__(self):
        self.secure_storage = SecureAccountStorage("data/accounts.secure.json")
        self.legacy_storage = Storage(folder="data")
        self.accounts, self.current_username = [], None
        self.load()

    def load(self):
        try: data = self.secure_storage.load()
        except (OSError, ValueError): data = None
        if data is None:
            data = self.legacy_storage.load("accounts")
            if data:
                self.accounts = data.get("accounts", []); self.current_username = data.get("current"); self.save(); self.legacy_storage.delete("accounts"); return
        self.accounts = (data or {}).get("accounts", []); self.current_username = (data or {}).get("current")

    def save(self): self.secure_storage.save({"accounts": self.accounts, "current": self.current_username})
    def find(self, username): return next((a for a in self.accounts if a.get("username") == username), None)
    def add_offline_account(self, username):
        existing = self.find(username)
        if existing:
            existing["type"] = "offline"
            for field in ("uuid", "access_token", "refresh_token"): existing.pop(field, None)
        else: self.accounts.append({"username": username, "type": "offline"})
        self.current_username = username; self.save()
    def add_premium_account(self, username, uuid, access_token, refresh_token=None):
        existing = self.find(username); values = {"type": "premium", "uuid": uuid, "access_token": access_token, "refresh_token": refresh_token}
        if existing: existing.update(values)
        else: self.accounts.append({"username": username, **values})
        self.current_username = username; self.save()
    def remove_account(self, username):
        self.accounts = [a for a in self.accounts if a.get("username") != username]
        if self.current_username == username: self.current_username = self.accounts[0]["username"] if self.accounts else None
        self.save()
    def get_accounts(self): return self.accounts
    def has_account(self, username): return self.find(username) is not None
    def set_current(self, username):
        if self.find(username): self.current_username = username; self.save()
    def get_current(self): return self.find(self.current_username) if self.current_username else None
