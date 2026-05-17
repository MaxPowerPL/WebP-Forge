"""
Pomocnicze funkcje formatowania i zarządzania wątkami.
"""
from __future__ import annotations

import threading
from datetime import datetime
from typing import Callable


# ── formatowanie rozmiaru pliku ───────────────────────────────────────────────

def format_bytes(size: int) -> str:
    """Zwraca czytelny rozmiar, np. '1.23 MB'."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size) < 1024.0:
            return f"{size:.2f} {unit}" if unit != "B" else f"{size} B"
        size /= 1024.0  # type: ignore[assignment]
    return f"{size:.2f} TB"


def format_timestamp(dt: datetime | None = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


# ── bezpieczne wywołania GUI z wątku roboczego ────────────────────────────────

def run_in_main_thread(widget, callback: Callable, *args) -> None:
    """Planuje wywołanie callback w głównym wątku Tk (after 0)."""
    try:
        widget.after(0, lambda: callback(*args))
    except Exception:
        pass


# ── prosty zamek cancel ───────────────────────────────────────────────────────

class CancelToken:
    """Prosty token anulowania bezpieczny wielowątkowo."""

    def __init__(self) -> None:
        self._cancelled = threading.Event()

    def cancel(self) -> None:
        self._cancelled.set()

    def reset(self) -> None:
        self._cancelled.clear()

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled.is_set()
