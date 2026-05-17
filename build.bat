@echo off

REM ─────────────────────────────────────────────────────────────────────────────
REM  WebP Forge – skrypt budowania .exe dla Windows
REM  Uruchom z aktywowanym venv: build.bat
REM ─────────────────────────────────────────────────────────────────────────────
echo [BUILD] WebP Forge – budowanie pliku .exe...
echo.

REM Sprawdz czy PyInstaller jest dostepny
pyinstaller --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [BLAD] PyInstaller nie zostal znaleziony. Zainstaluj: pip install pyinstaller
    pause
    exit /b 1
)

REM Wyczysc poprzednie buildy
echo [1/3] Czyszczenie poprzednich buildow...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

REM Buduj
echo [2/3] Kompilacja...
pyinstaller webp_forge.spec --clean --noconfirm
IF ERRORLEVEL 1 (
    echo [BLAD] Budowanie nie powiodlo sie.
    pause
    exit /b 1
)

echo [3/3] Gotowe!
echo.
echo Plik wykonywalny: dist\WebPForge.exe
echo.
pause