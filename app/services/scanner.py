"""
Serwis skanowania plików PNG z katalogu (rekurencyjnie).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def scan_png_files(source: Path) -> List[Path]:
    """
    Zwraca listę plików PNG z podanej ścieżki.
    Jeśli source to plik – zwraca listę jednoelementową.
    Jeśli source to katalog – skanuje rekurencyjnie.
    """
    if not source.exists():
        return []
    if source.is_file():
        if source.suffix.lower() == ".png":
            return [source]
        return []
    results: List[Path] = []
    for p in sorted(source.rglob("*.png")):
        if p.is_file():
            results.append(p)
    logger.info("Znaleziono %d plików PNG w: %s", len(results), source)
    return results


def resolve_output_path(
    source_file: Path,
    source_root: Path,
    output_root: Path,
    filename_behavior: str,
) -> Path:
    """
    Buduje docelową ścieżkę WebP zachowując względną strukturę katalogów.

    Args:
        source_file: bezwzględna ścieżka do pliku PNG.
        source_root: katalog bazowy (folder wybrany przez użytkownika, lub katalog pliku).
        output_root: katalog wyjściowy wybrany przez użytkownika.
        filename_behavior: 'keep' | 'suffix_webp' | 'hyphenate'
    """
    try:
        relative = source_file.relative_to(source_root)
    except ValueError:
        relative = Path(source_file.name)

    stem = relative.stem
    parent = relative.parent

    if filename_behavior == "suffix_webp":
        stem = stem + "_webp"
    elif filename_behavior == "hyphenate":
        stem = stem.replace(" ", "-")

    new_name = stem + ".webp"
    return output_root / parent / new_name


def apply_suffix_to_avoid_conflict(path: Path) -> Path:
    """Dodaje _1, _2, ... do nazwy pliku aż nie będzie konfliktu."""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
