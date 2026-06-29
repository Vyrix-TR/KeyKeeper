"""
Vaultify Pro - v1.0
Ana Çalıştırıcı ve CLI Menü
"""
import sys
import os
from getpass import getpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from crypto_core import VaultCrypto
from watcher import start_watch

console = Console()
vault = VaultCrypto()

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        menu = Table(title="🛡️ Vaultify PRO v1.0", box=None)
        menu.add_row("[1] Ekle [2] Oku [3] Listele [4] Sil [5] İzleyici [0] Çıkış")
        console.print(Panel(menu))
        
        sec = console.input("[bold yellow]Seçiminiz:[/] ")
        
        if sec == "1":
            p = console.input("Site/Platform Adı: ")
            t = "E-posta" if console.input("Giriş Tipi (1: E-posta, 2: Kullanıcı Adı): ") == "1" else "Kullanıcı Adı"
            k = console.input(f"{t}: ")
            s = getpass("Şifre (Yazarken gizlenir): ")
            if vault.add_record(p, t, k, s): 
                console.print("[green]✅ Başarıyla kaydedildi.[/]")
            
        elif sec == "2":
            p = console.input("Okunacak Platform: ")
            res = vault.get_record(p)
            if res: 
                console.print(f"\n[bold green]🔑 {res['tip']}:[/] {res['kimlik']} | [bold green]Şifre:[/] {res['sifre']}")
            else: 
                console.print("[red]❌ Kayıt bulunamadı.[/]")
            
        elif sec == "3":
            kayitlar = vault.list_records()
            if kayitlar: 
                console.print(f"\n📂 [bold]Kasadaki Platformlar:[/] {', '.join(kayitlar)}")
            else: 
                console.print("[yellow]📂 Kasa şu an boş.[/]")
            
        elif sec == "4":
            p = console.input("Silinecek Platform: ")
            if vault.delete_record(p): 
                console.print("[green]✅ Kayıt silindi.[/]")
            else: 
                console.print("[red]❌ Kayıt bulunamadı veya silinemedi.[/]")
        
        elif sec == "5": 
            start_watch(vault)
            
        elif sec == "0": 
            sys.exit()
            
        console.input("\nDevam etmek için [Enter]'a basın...")

if __name__ == "__main__":
    main()