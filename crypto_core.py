"""
Vaultify Pro - v1.0
Çekirdek Kripto ve Taşınabilir Veri Yönetimi Servisi
"""
import json
import os
from cryptography.fernet import Fernet

class VaultCrypto:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
        self.DATA_FILE = os.path.join(self.BASE_DIR, "vault_data.json")
        self.KEY_FILE = os.path.join(self.BASE_DIR, "secret.key")
        self.key = self._load_key()
        self.cipher = Fernet(self.key)
        self.db = self._load_db()

    def _load_key(self):
        if not os.path.exists(self.KEY_FILE):
            key = Fernet.generate_key()
            with open(self.KEY_FILE, "wb") as f:
                f.write(key)
            return key
        with open(self.KEY_FILE, "rb") as f:
            return f.read()

    def _load_db(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def add_record(self, platform, tip, kimlik, sifre):
        data = {"tip": tip, "kimlik": kimlik, "sifre": sifre}
        self.db[platform] = self.cipher.encrypt(json.dumps(data).encode()).decode()
        return self._save_db()

    def _save_db(self):
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.db, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False

    def get_record(self, platform):
        if platform in self.db:
            try:
                decrypted = self.cipher.decrypt(self.db[platform].encode()).decode()
                return json.loads(decrypted)
            except:
                return None
        return None

    def delete_record(self, platform):
        if platform in self.db:
            del self.db[platform]
            return self._save_db()
        return False

    def list_records(self):
        return sorted(list(self.db.keys()))