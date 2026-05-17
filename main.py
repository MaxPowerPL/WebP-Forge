"""
WebP Forge – punkt startowy aplikacji.
Uruchom: python main.py
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

# Upewnij się że katalog projektu jest na ścieżce importu
_ROOT = Path(__file__).parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Tworzenie katalogów danych jeśli nie istnieją
from app.config.constants import DATA_DIR, ASSETS_DIR, ICONS_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
ICONS_DIR.mkdir(parents=True, exist_ok=True)

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("webp_forge")


def main() -> None:
    logger.info("Uruchamianie WebP Forge...")
    try:
        from app.views.main_window import MainWindow
        app = MainWindow()
        app.protocol("WM_DELETE_WINDOW", app.on_close)
        app.mainloop()
    except Exception as exc:
        logger.critical("Krytyczny błąd aplikacji: %s", exc, exc_info=True)
        try:
            import tkinter.messagebox as mb
            mb.showerror("Błąd krytyczny", f"Aplikacja napotkała błąd:\n{exc}")
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
