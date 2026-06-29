"""
Vaultify Pro - v1.0
Ana Çalıştırıcı ve CLI Gelişmiş Görsel Menü
"""
import sys
import os
import time
from getpass import getpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from crypto_core import VaultCrypto
from watcher import start_watch

console = Console()
vault = VaultCrypto()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header():
    clear_screen()
    header_text = (
        "[bold green]⚡ VAULTIFY SİBER GÜVENLİK İSTASYONU ⚡[/]\n"
        "[dim]Bütünsel AES-256 Şifreleme ve Pano Yönetim Sistemi | Sürüm v1.0[/]"
    )
    console.print(Panel(Align.center(header_text), border_style="green", expand=False))
    print()

def authenticate():
    clear_screen()
    
    # 1. Durum: İlk Kurulum (Parola Belirleme)
    if vault.is_first_run():
        console.print(Panel(
            "[bold cyan][⚡] İLK KURULUM TESPİT EDİLDİ[/]\n\n"
            "[!] Lütfen bu kasaya erişmek için kullanacağınız bir [bold yellow]Master Password (Ana Parola)[/] belirleyin.\n"
            "[⚠️] Bu parolayı unutursanız verilerinize bir daha asla erişemezsiniz!",
            title="🔐 Vaultify Provisioning", border_style="cyan"
        ))
        while True:
            p1 = getpass("Yeni Ana Parola Oluşturun: ").strip()
            if not p1:
                console.print("[bold red]Parola boş bırakılamaz![/]")
                continue
            p2 = getpass("Parolayı Tekrar Girin: ").strip()
            
            if p1 == p2:
                vault.set_master_password(p1)
                console.print("\n[bold green]✅ Ana parola başarıyla oluşturuldu! Sistem başlatılıyor...[/]")
                time.sleep(2)
                break
            else:
                console.print("[bold red]❌ Parolalar eşleşmedi! Lütfen tekrar deneyin.[/]")
    
    # 2. Durum: Normal Giriş
    else:
        draw_header()
        console.print("[bold yellow]🔒 KASA KİLİTLİ[/]\n")
        attempts = 3
        while attempts > 0:
            passwd = getpass(f"Master Password Girin ({attempts} Hak): ").strip()
            if vault.verify_master_password(passwd):
                console.print("\n[bold green]🔓 ERİŞİM ONAYLANDI: Kasa başarıyla açıldı.[/]")
                time.sleep(1)
                return True
            else:
                attempts -= 1
                console.print("[bold red]❌ GEÇERSİZ PAROLA! Erişim reddedildi.[/]\n")
        
        console.print("[bold black on red]🛑 SİSTEM KİLİTLENDİ: Çok fazla hatalı deneme yapıldı.[/]")
        time.sleep(2)
        sys.exit()

def main():
    authenticate()
    
    while True:
        draw_header()
        
        menu_table = Table(box=None, expand=False)
        menu_table.add_column("Komut", style="bold yellow", justify="center")
        menu_table.add_column("Açıklama", style="bold white")
        
        menu_table.add_row("[1]", "🔐 Kasaya Yeni Şifreli Veri Ekle")
        menu_table.add_row("[2]", "🔍 Belirli Bir Platformun Şifresini Çöz / Oku")
        menu_table.add_row("[3]", "📂 Kasadaki Tüm Platformları Listele")
        menu_table.add_row("[4]", "❌ Kasadan Veri Sil")
        menu_table.add_row("[5]", "🤖 Akıllı Pano (Clipboard) İzleyicisini Başlat")
        menu_table.add_row("[0]", "🚪 Güvenli Çıkış Yap")
        
        console.print(Panel(menu_table, title="🤖 ANA KONTROL PANELİ", border_style="blue", expand=False))
        print()
        
        sec = console.input("[bold gold1]💻 Sistem Seçiminiz >>> [/] ").strip()
        
        if sec == "1":
            draw_header()
            console.print("[bold cyan]📝 YENİ KAYIT EKLEME EKRANI[/]\n")
            p = console.input("[bold]Platform / Site Adı:[/] ").strip()
            
            console.print("\n[1] E-posta\n[2] Kullanıcı Adı")
            t_sec = console.input("\nGiriş Tipi Seçimi (1 veya 2): ").strip()
            t = "E-posta" if t_sec == "1" else "Kullanıcı Adı"
            
            k = console.input(f"[bold]{t}:[/] ").strip()
            s = getpass("Şifre (Güvenlik için yazarken ekranda gizlenir): ")
            
            if vault.add_record(p, t, k, s): 
                console.print(f"\n[bold green]✅ BAŞARILI:[/] '{p}' veritabanına eklendi ve tüm dosya mühürlendi.")
            
        elif sec == "2":
            draw_header()
            console.print("[bold cyan]🔍 VERİ OKUMA / ŞİFRE ÇÖZME EKRANI[/]\n")
            p = console.input("[bold]Okunacak Platform Adı:[/] ").strip()
            res = vault.get_record(p)
            
            if res: 
                result_table = Table(title=f"🔑 '{p}' Hesabına Ait Bilgiler", border_style="green")
                result_table.add_column("Veri Tipi", style="yellow")
                result_table.add_column("Değer", style="bold white")
                result_table.add_row(res['tip'], res['kimlik'])
                result_table.add_row("Şifre", res['sifre'])
                
                print()
                console.print(result_table)
            else: 
                console.print(f"\n[bold red]❌ HATA:[/] Kasada '{p}' adına ait hiçbir şifreli kayıt bulunamadı.")
            
        elif sec == "3":
            draw_header()
            kayitlar = vault.list_records()
            if kayitlar: 
                list_table = Table(title="📂 Şifreli Kasada Duran Platformlar", border_style="magenta")
                list_table.add_column("No", justify="center", style="dim")
                list_table.add_column("Platform / Veri Adı", style="bold magenta")
                
                for idx, kayıt in enumerate(kayitlar, 1):
                    list_table.add_row(str(idx), kayıt)
                
                console.print(list_table)
            else: 
                console.print(Panel("[bold yellow]📂 Kasa şu an tamamen boş. Henüz şifreli veri eklenmemiş.[/]", border_style="yellow"))
            
        elif sec == "4":
            draw_header()
            console.print("[bold red]❌ VERİ SİLME EKRANI[/]\n")
            p = console.input("[bold]Silinecek Platform Adı:[/] ").strip()
            
            onay = console.input(f"[bold yellow][!] '{p}' kaydı kalıcı olarak silinecek. Onaylıyor musunuz? (e/h): [/]").lower().strip()
            if onay == 'e':
                if vault.delete_record(p): 
                    console.print(f"\n[bold green]✅ BAŞARILI:[/] '{p}' kaydı kasadan temizlendi ve dosya yeniden mühürlendi.")
                else: 
                    console.print(f"\n[bold red]❌ HATA:[/] '{p}' kaydı silinemedi veya bulunamadı.")
            else:
                console.print("\n[yellow]Silme işlemi kullanıcı tarafından iptal edildi.[/]")
        
        elif sec == "5": 
            draw_header()
            start_watch(vault)
            
        elif sec == "0": 
            draw_header()
            console.print("[bold red]🔒 Güvenli çıkış yapılıyor... Veritabanı kilitlendi.[/]")
            time.sleep(1)
            sys.exit()
            
        else: 
            console.print("[bold red]❌ Geçersiz komut! Lütfen menüdeki rakamlardan birini girin.[/]")
            
        console.input("\n[dim]Devam etmek için [Enter]'a basın...[/]")

if __name__ == "__main__":
    main()