"""
Model ustawień użytkownika – odczyt/zapis JSON.
"""
from __future__ import annotations

import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.config.constants import DEFAULT_SETTINGS, SETTINGS_FILE

logger = logging.getLogger(__name__)


class Settings:
    """Przechowuje ustawienia i synchronizuje je z plikiem JSON."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = deepcopy(DEFAULT_SETTINGS)
        self._path: Path = SETTINGS_FILE
        self.load()

    # ── public ────────────────────────────────────────────────────────────────

    def load(self) -> None:
        if self._path.exists():
            try:
                with self._path.open("r", encoding="utf-8") as f:
                    saved = json.load(f)
                # Merge – nowe klucze z defaults nie zostaną zgubione
                for key, value in saved.items():
                    if key in self._data:
                        self._data[key] = value
            except Exception as exc:
                logger.warning("Nie można wczytać ustawień: %s", exc)

    def save(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.error("Nie można zapisać ustawień: %s", exc)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    def update(self, data: dict[str, Any]) -> None:
        self._data.update(data)
        self.save()

    # ── convenience properties ────────────────────────────────────────────────

    @property
    def last_input_path(self) -> str:
        return self._data.get("last_input_path", "")

    @last_input_path.setter
    def last_input_path(self, v: str) -> None:
        self.set("last_input_path", v)

    @property
    def last_output_path(self) -> str:
        return self._data.get("last_output_path", "")

    @last_output_path.setter
    def last_output_path(self, v: str) -> None:
        self.set("last_output_path", v)

    @property
    def conversion_mode(self) -> str:
        return self._data.get("conversion_mode", "lossy")

    @conversion_mode.setter
    def conversion_mode(self, v: str) -> None:
        self.set("conversion_mode", v)

    @property
    def quality_preset(self) -> str:
        return self._data.get("quality_preset", "Wysoka")

    @quality_preset.setter
    def quality_preset(self, v: str) -> None:
        self.set("quality_preset", v)

    @property
    def filename_behavior(self) -> str:
        return self._data.get("filename_behavior", "keep")

    @filename_behavior.setter
    def filename_behavior(self, v: str) -> None:
        self.set("filename_behavior", v)

    @property
    def window_width(self) -> int:
        return self._data.get("window_width", 1100)

    @property
    def window_height(self) -> int:
        return self._data.get("window_height", 780)
