<div align="center">

  <img src="app/assets/icons/app.ico" alt="WebP Forge Logo" width="120" height="auto" />

  # WebP Forge

  **Zaawansowany konwerter PNG → WebP dla Windows z nowoczesnym ciemnym interfejsem.**
  <br>
  *Konwertuj pojedyncze pliki, całe foldery i partię plików – szybko, wielowątkowo i z pełną kontrolą jakości.*

  <p>
    <a href="https://github.com/MaxPowerPL/WebP-Forge/releases/tag/v1.0.0">
      <img src="https://img.shields.io/github/v/tag/MaxPowerPL/webp-forge?label=VERSION&style=for-the-badge&color=238636" alt="Wersja" />
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/Status-Stabilny-important?style=for-the-badge" alt="Status" />
    </a>
    <a href="https://www.python.org/downloads/release/python-3125/">
      <img src="https://img.shields.io/badge/Python-3.12.5-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12.5" />
    </a>
    <a href="https://github.com/TomSchimansky/CustomTkinter">
      <img src="https://img.shields.io/badge/GUI-CustomTkinter%205.2-FF5722?style=for-the-badge&logo=tkinter&logoColor=white" alt="CustomTkinter" />
    </a>
    <a href="https://github.com/MaxPowerPL/webp-forge/stargazers">
      <img src="https://img.shields.io/github/stars/MaxPowerPL/webp-forge?style=for-the-badge&color=yellow" alt="Stars" />
    </a>
    <a href="https://github.com/MaxPowerPL/webp-forge">
      <img src="https://img.shields.io/github/last-commit/MaxPowerPL/webp-forge?style=for-the-badge" alt="Last Commit" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
    </a>
  </p>

  <p>
    <a href="#-o-projekcie">📖 O Projekcie</a> •
    <a href="#-funkcjonalności">✨ Funkcjonalności</a> •
    <a href="#-technologie">🛠️ Technologie</a> •
    <a href="#-instalacja-i-uruchomienie">🚀 Instalacja</a> •
    <a href="#-struktura-projektu">📂 Struktura</a> •
    <a href="#%EF%B8%8F-roadmapa">🗺️ Roadmapa</a>
  </p>
</div>

---

## 📖 O Projekcie

**WebP Forge** to desktopowe narzędzie dla Windows 11 do masowej konwersji plików PNG do formatu WebP. Powstało z potrzeby posiadania szybkiego, wygodnego konwertera GUI, który nie wymaga wiedzy o liniach komend i nie zmusza do korzystania z narzędzi online.

Format WebP oferuje zazwyczaj 25–35% mniejszy rozmiar pliku w porównaniu do PNG przy zachowaniu tej samej wizualnej jakości. WebP Forge pozwala skorzystać z tej zalety bez utraty wygody: przeciągnij foldery, wybierz tryb, kliknij konwertuj. Aplikacja przetwarza pliki wielowątkowo i na bieżąco pokazuje postęp, logi i raport z zaoszczędzonego miejsca.

Projekt jest zbudowany na architekturze MVC i starannie podzielony na warstwy – modele danych, widoki CustomTkinter, kontrolery orkiestrujące logikę, serwisy konwersji i persystencji. Ustawienia i historia konwersji są automatycznie zapisywane do JSON.

### 🎯 Aktualna Wersja: `v1.0.0 (Stabilny)`

Pierwsza pełna wersja publiczna. Obsługuje konwersję pojedynczych plików, wsadową konwersję pliku i folderów z rekurencyjnym skanowaniem, tryby Lossless i Lossy z presetami jakości, obsługę przezroczystości (RGBA), zarządzanie konfliktami, anulowanie, historię i raport.

---

## ✨ Funkcjonalności

Co już działa w tej wersji?

- [x] **Wybór źródeł**:
  - Pojedynczy plik PNG (dialog wyboru pliku).
  - Wiele plików jednocześnie (dialog wielokrotnego wyboru).
  - Cały folder z rekurencyjnym skanowaniem podfolderów.
  - Zachowanie oryginalnej struktury katalogów w folderze wyjściowym.
- [x] **Wyjście**:
  - Dowolny katalog docelowy wybrany przez użytkownika.
  - Wyraźne pole pokazujące wybraną ścieżkę wyjściową.
- [x] **Tryby konwersji**:
  - Lossless (bezstratna jakość) – idealna dla grafik z tekstem.
  - Lossy (stratna jakość) – najlepszy stosunek jakości do rozmiaru dla zdjęć.
- [x] **Jakość Lossy**:
  - Presety: Niska (40), Średnia (65), Wysoka (82), Maksymalna (95).
  - Brak zgadywania wartości – czytelne etykiety po polsku.
- [x] **Przezroczystość**:
  - Automatyczne zachowanie kanału alpha (PNG RGBA → WebP z alpha).
- [x] **Obsługa konfliktów**:
  - Dialog pokazujący konkretną ścieżkę konfliktu z opcjami: Nadpisz / Pomiń / Dodaj sufiks `_1`.
- [x] **Postęp i status**:
  - Globalny pasek postępu, licznik plików, bieżąca nazwa pliku.
  - Okno logu z timestampami.
  - Podsumowanie po zakończeniu sesji.
- [x] **Raport GUI**:
  - Tabelaryczny raport: rozmiar PNG, rozmiar WebP, % zaoszczędzone, status.
- [x] **Historia konwersji**:
  - Persystentna historia w JSON z datą, ścieżką, trybem i oszczędnościami.
- [x] **Ustawienia użytkownika**:
  - Automatyczny zapis ostatnich ścieżek, trybu, jakości i zachowania nazw do JSON.
- [x] **Nazwy plików**:
  - Zachowaj oryginalne / dodaj `_webp` / zastąp spacje myślnikami.
- [x] **Anulowanie**:
  - Przycisk Anuluj bezpiecznie zatrzymuje kolejkę zadań.
- [x] **Wielowątkowość**:
  - Konwersja w puli wątków (domyślnie 4) – GUI pozostaje responsywny.
- [ ] **Drag & Drop** (W przygotowaniu):
  - Przeciąganie plików/folderów bezpośrednio do okna aplikacji.

---

## 🛠️ Technologie

Projekt został zbudowany przy użyciu:

| Technologia | Opis |
| :--- | :--- |
| **Python 3.12.5** | Główny język. Nowoczesna składnia, stabilny ekosystem. |
| **CustomTkinter 5.2** | Nowoczesna nakładka na Tkinter dająca ciemny, profesjonalny wygląd bez zewnętrznych frameworków Qt/wx. |
| **Pillow 10.4** | Silnik konwersji obrazów. Wbudowany libwebp w kołach Windows – zero dodatkowych binarnych zależności, pełna kontrola trybu lossless/lossy, natywna obsługa RGBA. |
| **ThreadPoolExecutor** | Wielowątkowa konwersja z stdlib – brak zewnętrznych zależności, bezpieczna integracja z Tk. |
| **JSON (stdlib)** | Persystencja ustawień i historii – lekki, czytelny, bez bazy danych. |
| **PyInstaller 6.11** | Pakowanie do samodzielnego `.exe` dla Windows. |

### Dlaczego Pillow, a nie opencv/imageio?

Pillow to najdojrzalsza, najszerzej wspierana biblioteka do obsługi obrazów w Pythonie. Koła dla Windows zawierają wbudowany `libwebp` – nie trzeba instalować żadnych dodatkowych binarnych zależności. `opencv-python` dodałby ~50 MB overhead i wiele niepotrzebnych zależności, `imageio` to tylko wrapper na inne biblioteki. Pillow daje bezpośrednią kontrolę nad jakością WebP, trybem lossless, metodą kompresji i zachowaniem alpha – wszystko czego ta aplikacja potrzebuje.

---

## 🚀 Instalacja i Uruchomienie

### 1. Wymagania

- Windows 10/11 (64-bit)
- Python 3.12.5 ([python.org](https://www.python.org/downloads/release/python-3125/))
- Git (opcjonalnie)

### 2. Klonowanie repozytorium

```bash
git clone https://github.com/MaxPowerPL/webp-forge.git
cd webp-forge
```

Lub pobierz jako ZIP z GitHub i wypakuj.

### 3. Konfiguracja środowiska wirtualnego

**Windows (PowerShell lub CMD):**

```bash
# Utwórz środowisko wirtualne
python -m venv venv

# Aktywuj venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Aktywuj venv (CMD)
venv\Scripts\activate.bat
```

> Jeśli PowerShell blokuje skrypt, uruchom: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 4. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 5. Uruchomienie

```bash
python main.py
```

### 6. Użytkowanie

- **Wybór plików**: Kliknij `Plik`, `Pliki` lub `Folder` w panelu lewym.
- **Cel**: Kliknij `Wybierz katalog wyjściowy`.
- **Ustawienia**: Wybierz tryb (Lossless/Lossy) i jakość z list rozwijanych.
- **Konwersja**: Kliknij `▶ Konwertuj`. Postęp jest widoczny na pasku i w logu.
- **Anulowanie**: Kliknij `⛔ Anuluj` aby zatrzymać kolejkę.
- **Raport**: Zakładka `📊 Raport` pokazuje wyniki każdego pliku.
- **Historia**: Zakładka `🕒 Historia` pokazuje poprzednie sesje.

---

## 📦 Budowanie pliku .exe (PyInstaller)

Aby zbudować samodzielny plik `.exe` niewymagający instalacji Pythona:

```bash
# Upewnij się, że venv jest aktywny i zależności zainstalowane
pyinstaller webp_forge.spec --clean --noconfirm
```

Lub użyj dołączonego skryptu:

```bash
build.bat
```

Wynikowy plik znajduje się w: `dist\WebPForge.exe`

### Uwagi do buildu

- Ikona: umieść `app.ico` w `app/assets/icons/` przed buildem (patrz `app/assets/icons/README.md`).
- Zasoby (`app/assets/`) są automatycznie dołączane przez spec.
- Flaga `console=False` wyłącza okno konsoli w finalnym `.exe`.
- UPX (`upx=True`) kompresuje binarki jeśli UPX jest zainstalowany i dostępny w PATH – zmniejsza rozmiar pliku o ~30%.

---

## 📂 Struktura Projektu

Projekt stosuje architekturę MVC z wyraźnym podziałem odpowiedzialności:

```text
📦 webp-forge
┣ 📂 app/
┃ ┣ 📂 config/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┗ 📜 constants.py       # Stałe: ścieżki, presety jakości, domyślne ustawienia
┃ ┣ 📂 controllers/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┗ 📜 conversion_controller.py  # Orkiestracja: skanowanie → zadania → konwersja → historia
┃ ┣ 📂 models/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┣ 📜 conversion_job.py  # Modele danych: ConversionJob, ConversionResult, JobStatus
┃ ┃ ┣ 📜 history.py         # Model historii konwersji + persystencja JSON
┃ ┃ ┗ 📜 settings.py        # Model ustawień + persystencja JSON
┃ ┣ 📂 services/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┣ 📜 converter.py       # Silnik konwersji PNG→WebP (Pillow)
┃ ┃ ┣ 📜 persistence.py     # Fabryki singletonów Settings i History
┃ ┃ ┗ 📜 scanner.py         # Skanowanie PNG, budowanie ścieżek wyjściowych
┃ ┣ 📂 utils/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┗ 📜 helpers.py         # format_bytes, format_timestamp, CancelToken, run_in_main_thread
┃ ┣ 📂 views/
┃ ┃ ┣ 📜 __init__.py
┃ ┃ ┣ 📜 conflict_dialog.py # Dialog wyboru akcji przy konflikcie pliku
┃ ┃ ┣ 📜 history_panel.py   # Panel historii (Treeview z poprzednimi sesjami)
┃ ┃ ┣ 📜 main_window.py     # Główne okno GUI (CustomTkinter)
┃ ┃ ┗ 📜 report_panel.py    # Panel raportu z tabelą wyników konwersji
┃ ┗ 📂 assets/
┃   ┗ 📂 icons/
┃     ┗ 📜 README.md         # Instrukcja tworzenia ikony app.ico
┣ 📂 data/
┃ ┣ 📜 settings.json         # Ustawienia użytkownika (auto-generowane)
┃ ┗ 📜 history.json          # Historia konwersji (auto-generowane)
┣ 📂 build/                  # Pliki tymczasowe PyInstaller (gitignore)
┣ 📂 docs/                   # Dodatkowa dokumentacja (opcjonalnie)
┣ 📜 main.py                 # Punkt startowy aplikacji
┣ 📜 requirements.txt        # Zależności Python
┣ 📜 webp_forge.spec         # Konfiguracja PyInstaller
┣ 📜 build.bat               # Skrypt budowania .exe (Windows)
┣ 📜 LICENSE                 # Licencja MIT
┗ 📜 README.md
```

### Opis głównych modułów

#### `app/config/`
| Plik | Opis |
|------|------|
| `constants.py` | Wszystkie stałe: ścieżki danych, presety jakości (Niska/Średnia/Wysoka/Maksymalna → wartości 40/65/82/95), etykiety trybów, domyślne ustawienia okna. |

#### `app/models/`
| Plik | Opis |
|------|------|
| `conversion_job.py` | Dataclassy `ConversionJob` (jedno zadanie) i `ConversionResult` (sesja). Enum `JobStatus`. Właściwości `size_saved_bytes` i `percent_saved`. |
| `settings.py` | Klasa `Settings` – odczyt/zapis JSON z automatycznym merge nowych kluczy. |
| `history.py` | Klasa `History` + dataclass `HistoryEntry` – lista poprzednich sesji, max 200 wpisów. |

#### `app/services/`
| Plik | Opis |
|------|------|
| `converter.py` | Funkcja `convert_png_to_webp()` – otwiera PNG, konwertuje do WebP (lossless lub lossy z method=6), zachowuje alpha. Nie rzuca wyjątków – błędy zapisuje w `job.error_message`. |
| `scanner.py` | `scan_png_files()` – rekurencyjne `rglob("*.png")`. `resolve_output_path()` – buduje ścieżkę wyjściową zachowując strukturę folderów. `apply_suffix_to_avoid_conflict()` – `_1`, `_2`, ... |
| `persistence.py` | Fabryki singletonów `get_settings()` i `get_history()` – jedna instancja na cały cykl życia aplikacji. |

#### `app/controllers/`
| Plik | Opis |
|------|------|
| `conversion_controller.py` | Główna logika konwersji: uruchamia wątek, skanuje pliki, buduje zadania, obsługuje konflikty przez callback `on_conflict`, konwertuje w `ThreadPoolExecutor`, zapisuje historię. Komunika się z GUI wyłącznie przez callbacki. |

#### `app/views/`
| Plik | Opis |
|------|------|
| `main_window.py` | Główne okno CustomTkinter – nagłówek, lewy panel ustawień, prawy panel z postępem, zakładki Log/Raport/Historia. Okablowuje callbacki kontrolera. |
| `conflict_dialog.py` | Modal `CTkToplevel` – wyświetla ścieżkę konfliktu, czeka na decyzję użytkownika (Nadpisz/Pomiń/Sufiks). Thread-safe przez `threading.Event`. |
| `report_panel.py` | `ttk.Treeview` z kolorowymi wierszami – zielony/czerwony/żółty dla statusów OK/Błąd/Pominięto. |
| `history_panel.py` | Tabela poprzednich sesji z przyciskiem czyszczenia historii. |

---

## ⚙️ Szczegóły Konwersji WebP

### Tryby i jakość

| Tryb | Zastosowanie | Ustawienie Pillow |
|------|-------------|-------------------|
| **Lossless** | Grafiki, ikony, screenshoty z tekstem | `lossless=True` |
| **Lossy – Niska** | Thumbnaily, miniatury | `quality=40, method=6` |
| **Lossy – Średnia** | Ogólne użycie webowe | `quality=65, method=6` |
| **Lossy – Wysoka** | Domyślny – zdjęcia, blogi | `quality=82, method=6` |
| **Lossy – Maksymalna** | Archiwum, produkcja premium | `quality=95, method=6` |

`method=6` to najwolniejsza, ale najlepsza kompresja libwebp – w kontekście desktopowym (nie real-time) jest właściwym wyborem.

### Przezroczystość

- PNG z trybem `RGBA` → WebP zachowuje kanał alpha automatycznie.
- PNG z trybem `P` (paleta) lub `LA` → konwertowane do `RGBA` przed zapisem.
- PNG `RGB` bez alpha → konwertowane do `RGB` (mniejszy plik).

---

## 🗺️ Roadmapa

### Faza 1: Fundament (✅ Ukończone – v1.0.0)
- [x] Architektura MVC
- [x] Konwersja PNG → WebP (Lossless + Lossy)
- [x] Wielowątkowa konwersja z anulowaniem
- [x] Zachowanie przezroczystości
- [x] Rekurencyjne skanowanie folderów
- [x] Dialog konfliktu pliku
- [x] Raport i historia w GUI
- [x] Persystencja ustawień JSON
- [x] Build PyInstaller

### Faza 2: Ulepszenia UX (⏳ Planowane)
- [ ] Drag & Drop (tkinterdnd2)
- [ ] Podgląd miniatury wybranego pliku
- [ ] Porównanie PNG vs WebP side-by-side
- [ ] Eksport raportu do CSV/HTML
- [ ] Powiadomienie Windows po zakończeniu (toast notification)

### Faza 3: Rozszerzenia (💡 Pomysły)
- [ ] Wsparcie dla innych formatów wejściowych (JPEG, BMP, TIFF → WebP)
- [ ] Wsadowe przetwarzanie przez CLI (opcjonalne)
- [ ] Integracja z prawym przyciskiem myszy w Eksploratorze Windows (shell extension)
- [ ] Automatyczna aktualizacja (check for updates)

---

## 🐛 Znane Problemy i Rozwiązania

### ✅ Rozwiązane w v1.0.0

- **Zamrożenie GUI podczas konwersji**: Rozwiązane przez `ThreadPoolExecutor` – GUI pozostaje responsywny.
- **Utrata struktury podfolderów**: Naprawione przez `resolve_output_path()` z `relative_to()`.
- **Konflikt aktualizacji GUI z wątku roboczego**: Rozwiązane przez `widget.after(0, callback)` (run_in_main_thread).
- **Blokowanie wątku roboczego przez dialog konfliktu**: Rozwiązane przez `threading.Event` – dialog uruchamia się w main thread, wątek roboczy czeka na decyzję.

### 🔧 Znane ograniczenia

- [ ] Drag & Drop wymaga opcjonalnej biblioteki `tkinterdnd2` – nie jest dołączona domyślnie ze względu na potencjalne problemy z instalacją na niektórych konfiguracjach Windows.
- [ ] Okno konfliktu pojawia się osobno dla każdego konfliktu – przy dużych batchach z wieloma konfliktami może wymagać wielu kliknięć (planowane: opcja "zastosuj do wszystkich").
- [ ] Na bardzo wolnych dyskach sieciowych (NAS, UNC) skanowanie może zająć chwilę przed wyświetleniem postępu.

---

## 📝 Changelog

### v1.0.0 (Pierwsze wydanie publiczne)

**Nowe funkcje:**
- Pełne GUI w CustomTkinter z ciemnym motywem
- Konwersja lossless i lossy z presetami jakości po polsku
- Wielowątkowa konwersja (ThreadPoolExecutor, domyślnie 4 wątki)
- Rekurencyjne skanowanie folderów z zachowaniem struktury
- Obsługa przezroczystości PNG (RGBA, P, LA)
- Dialog konfliktu pliku (Nadpisz / Pomiń / Sufiks)
- Pasek postępu, log z timestampami, licznik plików
- Tabelaryczny raport konwersji z % zaoszczędzonego miejsca
- Historia konwersji persystowana w JSON
- Ustawienia użytkownika persystowane w JSON
- Opcje nazewnictwa plików (keep / _webp suffix / hyphenate)
- Anulowanie z bezpiecznym zatrzymaniem kolejki
- Budowanie do .exe przez PyInstaller

**Zmiany techniczne:**
- Architektura MVC: controllers / models / views / services / utils / config
- Komunikacja GUI ↔ kontroler wyłącznie przez callbacki (zero zależności widok→logika)
- Thread-safe aktualizacje GUI przez `widget.after(0, ...)`
- Singleton persistence przez `get_settings()` / `get_history()`

---

## 📜 Licencja

Ten projekt jest udostępniony na licencji **MIT**.

### Co MOŻESZ robić:

- ✅ Używać komercyjnie i prywatnie
- ✅ Modyfikować i dystrybuować dowolnie
- ✅ Dołączać do własnych projektów
- ✅ Sublicencjonować

### Czego NIE MOŻESZ robić bez zgody:

- ❌ Usuwać informacji o prawach autorskich
- ❌ Podawać się za autora oryginalnego projektu
- ❌ Twierdzić, że autor ponosi odpowiedzialność za ewentualne szkody

### Użytek komercyjny

Licencja MIT zezwala na użytek komercyjny bez konieczności informowania autora. Zachowaj jedynie informację o prawach autorskich w kodzie źródłowym lub dokumentacji.

Zobacz pełne warunki prawne w pliku [LICENSE](LICENSE).

---

<div align="center">

### ⭐ Jeśli podoba Ci się ten projekt, zostaw gwiazdkę na GitHubie! ⭐

☕ Stworzono używając Python + CustomTkinter + Pillow.
<br>
<sub>Projekt stworzony jako narzędzie produkcyjne i portfolio piece dla Windows 11.</sub>
<br>
<sub>**MIT License** – wolne oprogramowanie, używaj jak chcesz. Zobacz [LICENSE](LICENSE) po szczegóły.</sub>

<p>
  <a href="https://github.com/MaxPowerPL/webp-forge/issues/new?template=bug_report.yml">🐛 Zgłoś Bug</a> •
  <a href="https://github.com/MaxPowerPL/webp-forge/issues/new?template=feature_request.yml">💡 Zaproponuj Funkcję</a> •
  <a href="https://github.com/MaxPowerPL/webp-forge/wiki">📖 Wiki</a>
</p>

![Status](https://img.shields.io/badge/Status-Stabilny-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)

</div>
