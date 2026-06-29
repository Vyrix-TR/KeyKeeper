"""
Vaultify Pro - CLI Arayüzü
Görsel ve operasyonel yönetim paneli.
"""
import sys, os
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
        menu = Table(title="🛡️ Vaultify Pro v2.0", show_header=False, box=None)
        menu.add_row("[bold cyan]1.[/] ➕ Yeni Kayıt Ekle")
        menu.add_row("[bold cyan]2.[/] 🔍 Kayıt Oku")
        menu.add_row("[bold cyan]3.[/] 📂 Listele")
        menu.add_row("[bold cyan]4.[/] 🗑️ Sil")
        menu.add_row("[bold cyan]5.[/] 👀 İzleyici")
        menu.add_row("[bold red]0.[/] ❌ Çıkış")
        console.print(Panel(menu, expand=False))
        
        sec = console.input("[bold yellow]👉 Seçim:[/]")
        
        if sec == "1":
            p = console.input("[green]Site Adı:[/]").strip()
            t = "E-posta" if console.input("[green]1-Eposta, 2-Kullanıcı Adı:[/]") == "1" else "Kullanıcı Adı"
            i = console.input(f"[green]{t}:[/]").strip()
            s = getpass("Şifre (Gizli): ").strip()
            if p and i and s:
                if vault.add_record(p, t, i, s): console.print("[bold green]✅ Kaydedildi.[/]")
        
        elif sec == "2":
            p = console.input("[yellow]Platform:[/]")
            res = vault.get_record(p)
            if res:
                console.print(Panel(f"[bold cyan]Tip:[/] {res['tip']}\n[bold cyan]ID:[/] {res['id']}\n[bold cyan]Şifre:[/] {res['sifre']}", title=f"🔍 {p.upper()}"))
            else: console.print("[bold red]❌ Kayıt yok.[/]")
            
        elif sec == "3":
            table = Table(title="📂 Tüm Kayıtlar")
            for p in vault.list_records(): table.add_row(p)
            console.print(table)
            
        elif sec == "4":
            p = console.input("[red]Silinecek:[/]")
            if vault.delete_record(p): console.print("[bold red]✅ Silindi.[/]")
            
        elif sec == "5": start_watch(vault)
        elif sec == "0": sys.exit()
        
        console.input("\n[dim]Devam etmek için Enter...[/]")

if __name__ == "__main__":
    main()