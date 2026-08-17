import base64
import ctypes
import json
import os
from ctypes import wintypes


class _DataBlob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob(data):
    buffer = ctypes.create_string_buffer(data)
    return _DataBlob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer


class SecureAccountStorage:
    """Windows DPAPI store. Data is decryptable only by the current Windows user."""
    def __init__(self, file="data/accounts.secure.json"):
        self.file = file
        self.crypt32 = ctypes.windll.crypt32
        self.kernel32 = ctypes.windll.kernel32

    def _protect(self, data):
        source, keepalive = _blob(data); target = _DataBlob()
        if not self.crypt32.CryptProtectData(ctypes.byref(source), "SokoClient accounts", None, None, None, 0, ctypes.byref(target)):
            raise OSError("Nie udało się zaszyfrować danych konta w Windows DPAPI.")
        try: return base64.b64encode(ctypes.string_at(target.pbData, target.cbData)).decode("ascii")
        finally: self.kernel32.LocalFree(target.pbData)

    def _unprotect(self, encoded):
        source, keepalive = _blob(base64.b64decode(encoded)); target = _DataBlob(); description = ctypes.c_wchar_p()
        if not self.crypt32.CryptUnprotectData(ctypes.byref(source), ctypes.byref(description), None, None, None, 0, ctypes.byref(target)):
            raise OSError("Nie można odszyfrować danych konta dla tego użytkownika Windows.")
        try: return ctypes.string_at(target.pbData, target.cbData)
        finally: self.kernel32.LocalFree(target.pbData)

    def load(self):
        if not os.path.exists(self.file): return None
        with open(self.file, "r", encoding="utf-8") as handle: envelope = json.load(handle)
        if envelope.get("scheme") != "windows-dpapi": raise ValueError("Nieobsługiwany format bezpiecznych danych konta.")
        return json.loads(self._unprotect(envelope["payload"]).decode("utf-8"))

    def save(self, data):
        os.makedirs(os.path.dirname(self.file) or ".", exist_ok=True)
        envelope = {"scheme": "windows-dpapi", "payload": self._protect(json.dumps(data, ensure_ascii=False).encode("utf-8"))}
        temporary = self.file + ".tmp"
        with open(temporary, "w", encoding="utf-8") as handle: json.dump(envelope, handle)
        os.replace(temporary, self.file)
