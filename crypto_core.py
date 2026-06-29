"""
Vaultify Pro - v1.0
Bütünsel Dosya Şifreleme ve Kripto Çekirdek Motoru
"""
import json
import os
import hashlib
from cryptography.fernet import Fernet

class VaultCrypto:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
        self.DATA_FILE = os.path.join(self.BASE_DIR, "vault_data.json")
        self.KEY_FILE = os.path.join(self.BASE_DIR, "secret.key")
        self.PASS_FILE = os.path.join(self.BASE_DIR, "master.passwd")
        
        # 1. İlk çalışmada tamamen rastgele anahtar üretimi ve yüklemesi
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
        
        # 2. Şifrelenmiş tüm dosya içeriğini çözerek belleğe al
        self.db = self._load_db()

    def _load_or_generate_key(self):
        """Eğer anahtar yoksa ilk açılışta tamamen rastgele bir key üretir."""
        if not os.path.exists(self.KEY_FILE):
            random_key = Fernet.generate_key()
            with open(self.KEY_FILE, "wb") as f:
                f.write(random_key)
            return random_key
        with open(self.KEY_FILE, "rb") as f:
            return f.read()

    def _load_db(self):
        """Dosyanın tüm içeriğini tek seferde çözer ve JSON olarak okur."""
        if os.path.exists(self.DATA_FILE) and os.path.getsize(self.DATA_FILE) > 0:
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    encrypted_blob = f.read().strip()
                
                if not encrypted_blob:
                    return {}
                
                # Tüm dosya içeriğinin şifresini çözüyoruz
                decrypted_blob = self.cipher.decrypt(encrypted_blob.encode()).decode()
                return json.loads(decrypted_blob)
            except:
                # Herhangi bir bozulma veya geçersiz anahtar durumunda boş kasa döner
                return {}
        return {}

    def _save_db(self):
        """Kasadaki tüm verileri JSON yapıp, dosya içeriğinin tamamını şifreleyerek kaydeder."""
        try:
            plain_json_text = json.dumps(self.db, indent=4, ensure_ascii=False)
            # Tüm içeriği tek seferde AES-256 ile şifreliyoruz
            encrypted_blob = self.cipher.encrypt(plain_json_text.encode()).decode()
            
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                f.write(encrypted_blob)
            return True
        except:
            return False

    def is_first_run(self):
        return not os.path.exists(self.PASS_FILE)

    def set_master_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open(self.PASS_FILE, "w", encoding="utf-8") as f:
            f.write(hashed_password)
        return True

    def verify_master_password(self, password):
        if not os.path.exists(self.PASS_FILE):
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with open(self.PASS_FILE, "r", encoding="utf-8") as f:
            saved_hash = f.read().strip()
        return hashed_password == saved_hash

    def add_record(self, platform, tip, kimlik, sifre):
        # Verileri ham olarak sözlüğe ekleyip, kaydederken tüm dosyayı şifreliyoruz
        self.db[platform] = {"tip": tip, "kimlik": kimlik, "sifre": sifre}
        return self._save_db()

    def get_record(self, platform):
        return self.db.get(platform, None)

    def delete_record(self, platform):
        if platform in self.db:
            del self.db[platform]
            return self._save_db()
        return False

    def list_records(self):
        return sorted(list(self.db.keys()))