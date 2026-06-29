"""
Vaultify Pro - v1.0
Akıllı Pano İzleme Servisi (Görsel CLI Sürümü)
"""
import time
import pyperclip
from rich.console import Console
from rich.panel import Panel

console = Console()

def start_watch(vault_instance):
    console.print(Panel(
        "[bold cyan][!] AKILLI PANO İZLEYİCİ AKTİF EDİLDİ[/]\n\n"
        "[🛸] Sistem arka planda kopyalama işlemlerini dinliyor.\n"
        "[🔄] [bold yellow]Sıralama:[/] Önce Giriş Kimliğini (E-posta/ID), ardından Şifreyi kopyalayın.",
        title="🤖 Vaultify Watcher Engine", border_style="cyan"
    ))
    
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
                    console.print(f"\n[bold magenta][⚡] Veri Yakalandı (ID/E-posta):[/] [white on magenta] {id_data} [/]")
                    console.print("[bold yellow][>] Harika! Şimdi bu hesaba ait ŞİFREYİ kopyalayın...[/]")
                else:
                    password = cur
                    console.print(f"[bold magenta][⚡] Veri Yakalandı (Şifre):[/] [bold black on yellow] ******** [/]")
                    
                    console.print("\n" + "─" * 40)
                    plat = console.input("[bold green][?] Bu verilerin ait olduğu Platform/Site Adı nedir?: [/]").strip()
                    tip = "E-posta" if "@" in id_data else "Kullanıcı Adı"
                    
                    if vault_instance.add_record(plat, tip, id_data, password):
                        console.print(f"\n[bold green]✅ BAŞARILI:[/] '{plat}' verileri bütünsel bütünlüğe eklenerek şifrelendi.")
                        time.sleep(2)
                        return
            time.sleep(0.5)
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Pano izleyici kullanıcı tarafından sonlandırıldı.[/]")