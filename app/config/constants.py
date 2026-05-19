"""
WebP Forge – stałe konfiguracyjne aplikacji.
"""

APP_NAME = "WebP Forge"
APP_VERSION = "1.0.0"
APP_AUTHOR = "MaxPowerPL"
APP_DESCRIPTION = "Zaawansowany konwerter PNG/JPG → WebP"

# ─── Obsługiwane formaty wejściowe ────────────────────────────────────────────
SUPPORTED_EXTENSIONS: tuple[str, ...] = (".png", ".jpg", ".jpeg")
GITHUB_URL = "https://github.com/MaxPowerPL/webp-forge"

# ─── Ścieżki danych ────────────────────────────────────────────────────────────
import os
from pathlib import Path

_BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
DATA_DIR = _BASE_DIR / "data"
ASSETS_DIR = _BASE_DIR / "app" / "assets"
ICONS_DIR = ASSETS_DIR / "icons"

SETTINGS_FILE = DATA_DIR / "settings.json"
HISTORY_FILE = DATA_DIR / "history.json"

# ─── Predefiniowane jakości lossy ─────────────────────────────────────────────
QUALITY_PRESETS: dict[str, int] = {
    "Niska": 40,
    "Średnia": 65,
    "Wysoka": 82,
    "Maksymalna": 95,
}

DEFAULT_QUALITY_PRESET = "Wysoka"

# ─── Tryby konwersji ───────────────────────────────────────────────────────────
CONVERSION_MODE_LOSSLESS = "lossless"
CONVERSION_MODE_LOSSY = "lossy"

CONVERSION_MODE_LABELS: dict[str, str] = {
    CONVERSION_MODE_LOSSLESS: "Lossless (bezstratna jakość)",
    CONVERSION_MODE_LOSSY: "Lossy (stratna jakość)",
}

# ─── Opcje nazw plików ────────────────────────────────────────────────────────
FILENAME_KEEP = "keep"
FILENAME_SUFFIX_WEBP = "suffix_webp"
FILENAME_HYPHENATE = "hyphenate"

FILENAME_LABELS: dict[str, str] = {
    FILENAME_KEEP: "Zachowaj oryginalne nazwy",
    FILENAME_SUFFIX_WEBP: "Dodaj sufiks _webp",
    FILENAME_HYPHENATE: "Zastąp spacje myślnikami",
}

# ─── Opcje konfliktu plików ───────────────────────────────────────────────────
CONFLICT_OVERWRITE = "overwrite"
CONFLICT_SKIP = "skip"
CONFLICT_SUFFIX = "suffix"

# ─── Ustawienia domyślne ──────────────────────────────────────────────────────
DEFAULT_SETTINGS: dict = {
    "last_input_path": "",
    "last_output_path": "",
    "conversion_mode": CONVERSION_MODE_LOSSY,
    "quality_preset": DEFAULT_QUALITY_PRESET,
    "filename_behavior": FILENAME_KEEP,
    "theme": "dark",
    "window_width": 1100,
    "window_height": 780,
}

# ─── UI ───────────────────────────────────────────────────────────────────────
LOG_MAX_LINES = 500
HISTORY_MAX_ENTRIES = 200
MAX_WORKER_THREADS = 4
