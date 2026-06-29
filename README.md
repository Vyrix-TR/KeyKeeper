# 🔐 Vaultify Pro (KeyKeeper)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-Supported-orange?style=for-the-badge&logo=git&logoColor=white)
![UI](https://img.shields.io/badge/UI-Rich%20CLI-magenta?style=for-the-badge)

Vaultify Pro, hassas verilerinizi ve şifrelerinizi yerel bilgisayarınızda bütünsel veri şifreleme standartları kullanarak saklamanızı, yönetmenizi ve panonuzu (clipboard) izlemenizi sağlayan gelişmiş bir terminal (CLI) aracıdır.

---

## 🚀 Öne Çıkan Özellikler

* 📦 **Bütünsel Veritabanı Şifreleme:** `vault_data.json` dosyasının tamamı AES-256 (Fernet) ile şifrelenir. Dışarıdan bakıldığında platform isimleri dahil hiçbir veri okunamaz.
* 🎲 **Rastgele Anahtar Üretimi:** İlk çalıştırmada arka planda tamamen rastgele ve benzersiz bir `secret.key` dosyası inşa edilir.
* 🔑 **Master Password Koruması:** Kasaya erişimler SHA-256 hash altyapısı ile korunur. Hatalı denemelerde sistem kendini anında kilitler.
* 🤖 **Akıllı Pano (Clipboard) İzleyici:** Kopyalanan ID/E-posta ve şifre ikilisini havada yakalayarak doğrudan şifreleyip kasaya kilitler.
* 🎨 **Gelişmiş Görsel CLI:** `rich` kütüphanesinin dinamik panelleri ve temiz tabloları ile profesyonel bir terminal deneyimi sunar.

---

## 📂 Proje Yapısı

| Dosya / Klasör | Görevi |
| :--- | :--- |
| `crypto_core.py` | AES-256 şifreleme, bütünsel JSON veritabanı yönetimi ve SHA-256 şifre kontrolü. |
| `watcher.py` | Arka plan kopyalamalarını (clipboard) izleyen dinamik servis. |
| `vlt.py` | Ana kontrol paneli, kimlik doğrulama katmanı ve kullanıcı arayüzü. |
| `vlt.bat` | Windows işletim sistemlerinde tek tıkla uygulamayı başlatan başlatıcı betik. |
| `.gitignore` | Gizli kalması gereken yerel dosyaların Git takibine girmesini engeller. |
| `requirements.txt` | Uygulamanın çalışması için gerekli harici kütüphanelerin listesi. |

---

## 🛠️ Kurulum ve Çalıştırma

**1. Bağımlılıkların Yüklenmesi**
Terminali proje dizininde açın ve şu komutu çalıştırın:
```bash
pip install -r requirements.txt
