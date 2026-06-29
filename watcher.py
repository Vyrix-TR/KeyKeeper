"""
Vaultify Pro - v1.0
Akıllı Pano İzleme Servisi
"""
import time
import pyperclip

def start_watch(vault_instance):
    print("\n[!] İZLEYİCİ AKTİF (v1.0)")
    print("[!] Şu andan itibaren yapılan YENİ kopyalamalar izleniyor.")
    print("[!] Sırasıyla: Önce ID/E-posta, sonra Şifre kopyalayın.\n")
    
    try:
        last_val = pyperclip.paste()
    except:
        last_val = ""
        
    id_data = None
    
    try:
        while True:
            try:
                cur = pyperclip.paste().strip()
            except:
                cur = ""
            
            if cur != last_val and len(cur) > 0:
                last_val = cur
                
                if id_data is None:
                    id_data = cur
                    print(f"\n[+] ID/E-posta yakalandı: {id_data}")
                    print("[>] Şimdi Şifreyi kopyalayın...")
                else:
                    password = cur
                    plat = input("[?] Site Adı nedir?: ")
                    tip = "E-posta" if "@" in id_data else "Kullanıcı Adı"
                    
                    if vault_instance.add_record(plat, tip, id_data, password):
                        print("✅ Başarıyla kasaya kaydedildi. Menüye dönülüyor...")
                        time.sleep(1.5)
                        return
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] İzleyici kapatıldı.")