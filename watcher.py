import time, pyperclip

def start_watch(vault_instance):
    print("\n[!] İZLEYİCİ AKTİF.")
    print("[!] Şu andan itibaren yaptığın kopyalamalar (Ctrl+C) izleniyor.")
    print("[!] Önce ID/E-posta kopyala, sonra Şifreni kopyala.\n")
    
    # 1. Başlangıçta panoda ne varsa temizle/yoksay (Programı açtığın anı referans al)
    last_val = pyperclip.paste()
    id_data = None
    
    try:
        while True:
            cur = pyperclip.paste().strip()
            
            # 2. Sadece panodaki içerik DEĞİŞTİYSE ve boş değilse işlem yap
            if cur != last_val and len(cur) > 0:
                last_val = cur
                
                if id_data is None:
                    # ID/E-posta yakalama
                    id_data = cur
                    print(f"\n[+] ID/E-posta yakalandı: {id_data}")
                    print("[>] Şimdi Şifreyi kopyala...")
                else:
                    # Şifre yakalama
                    password = cur
                    plat = input("[?] Site Adı: ")
                    
                    tip = "E-posta" if "@" in id_data else "Kullanıcı Adı"
                    
                    if vault_instance.add_record(plat, tip, id_data, password):
                        print("✅ Başarıyla kaydedildi. Ana menüye dönülüyor...")
                        time.sleep(1)
                        return # Otomatik çıkış
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] İzleyici durduruldu.")