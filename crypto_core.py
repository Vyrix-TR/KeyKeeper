"""
Vaultify - Veri ve Şifreleme Modülü
Sorumluluk: Veritabanı işlemleri, AES-256 Şifreleme.
"""
import json
import os
from cryptography.fernet import Fernet

# Çalışma dizinini sabitle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "vault_data.json")
KEY_FILE = os.path.join(BASE_DIR, "secret.key")

class VaultCrypto:
    def __init__(self):
        self.key = self._load_key()
        self.cipher = Fernet(self.key)
        self.db = self._load_db()

    def _load_key(self):
        if not os.path.exists(KEY_FILE):
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as f: f.write(key)
            return key
        with open(KEY_FILE, "rb") as f: return f.read()

    def _load_db(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except: return {}
        return {}

    def _save_db(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.db, f, indent=4)
            return True
        except: return False

    def add_record(self, platform, tip, id_value, password):
        data = {"tip": tip, "id": id_value, "sifre": password}
        encrypted = self.cipher.encrypt(json.dumps(data).encode()).decode()
        self.db[platform] = encrypted
        return self._save_db()

    def get_record(self, platform):
        if platform in self.db:
            try:
                decrypted = self.cipher.decrypt(self.db[platform].encode()).decode()
                return json.loads(decrypted)
            except: return None
        return None

    def delete_record(self, platform):
        if platform in self.db:
            del self.db[platform]
            return self._save_db()
        return False

    def list_records(self):
        return sorted(list(self.db.keys()))