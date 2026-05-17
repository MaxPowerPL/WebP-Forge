"""
Serwis persystencji – opakowuje dostęp do Settings i History.
"""
from __future__ import annotations

from app.models.history import History, HistoryEntry
from app.models.settings import Settings

_settings: Settings | None = None
_history: History | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_history() -> History:
    global _history
    if _history is None:
        _history = History()
    return _history
