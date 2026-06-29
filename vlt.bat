@echo off
chcp 65001 >nul

:: Önce dosyaların olduğu klasöre git
cd /d "C:\Users\ahmet\Desktop\KeyKeep"

:: Şimdi kodu çalıştır
python "vlt.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Bir hata olustu! 
    pause
)