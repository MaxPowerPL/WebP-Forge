"""
Model historii konwersji – zapis/odczyt JSON.
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from app.config.constants import HISTORY_FILE, HISTORY_MAX_ENTRIES

logger = logging.getLogger(__name__)


@dataclass
class HistoryEntry:
    timestamp: str
    source_path: str
    output_path: str
    total_files: int
    done_files: int
    skipped_files: int
    error_files: int
    mode: str
    quality_preset: str
    total_saved_bytes: int
    total_source_bytes: int

    @classmethod
    def from_dict(cls, d: dict) -> "HistoryEntry":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})

    @property
    def percent_saved(self) -> float:
        if self.total_source_bytes > 0:
            return round(self.total_saved_bytes / self.total_source_bytes * 100, 1)
        return 0.0

    @property
    def timestamp_friendly(self) -> str:
        try:
            dt = datetime.fromisoformat(self.timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return self.timestamp


class History:
    """Przechowuje i persystuje historię konwersji."""

    def __init__(self) -> None:
        self._entries: List[HistoryEntry] = []
        self._path: Path = HISTORY_FILE
        self.load()

    # ── public ────────────────────────────────────────────────────────────────

    def load(self) -> None:
        if self._path.exists():
            try:
                with self._path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._entries = [HistoryEntry.from_dict(r) for r in raw if isinstance(r, dict)]
            except Exception as exc:
                logger.warning("Nie można wczytać historii: %s", exc)

    def save(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as f:
                json.dump([asdict(e) for e in self._entries], f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.error("Nie można zapisać historii: %s", exc)

    def add(self, entry: HistoryEntry) -> None:
        self._entries.insert(0, entry)
        if len(self._entries) > HISTORY_MAX_ENTRIES:
            self._entries = self._entries[:HISTORY_MAX_ENTRIES]
        self.save()

    def clear(self) -> None:
        self._entries = []
        self.save()

    @property
    def entries(self) -> List[HistoryEntry]:
        return list(self._entries)
