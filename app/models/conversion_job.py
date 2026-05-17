"""
Modele danych dla zadań konwersji i wyników.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path


class JobStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    DONE = auto()
    SKIPPED = auto()
    ERROR = auto()
    CANCELLED = auto()


@dataclass
class ConversionJob:
    """Pojedyncze zadanie konwersji – jeden plik PNG."""

    source_path: Path
    output_path: Path
    mode: str          # 'lossless' | 'lossy'
    quality: int       # wartość 1-100 (używana tylko w lossy)
    filename_behavior: str  # 'keep' | 'suffix_webp' | 'hyphenate'

    status: JobStatus = JobStatus.PENDING
    error_message: str = ""
    source_size_bytes: int = 0
    output_size_bytes: int = 0

    @property
    def size_saved_bytes(self) -> int:
        if self.status == JobStatus.DONE:
            return max(0, self.source_size_bytes - self.output_size_bytes)
        return 0

    @property
    def percent_saved(self) -> float:
        if self.source_size_bytes > 0 and self.status == JobStatus.DONE:
            return round(self.size_saved_bytes / self.source_size_bytes * 100, 1)
        return 0.0


@dataclass
class ConversionResult:
    """Zbiorczy wynik całej sesji konwersji."""

    jobs: list[ConversionJob] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.jobs)

    @property
    def done(self) -> int:
        return sum(1 for j in self.jobs if j.status == JobStatus.DONE)

    @property
    def skipped(self) -> int:
        return sum(1 for j in self.jobs if j.status == JobStatus.SKIPPED)

    @property
    def errors(self) -> int:
        return sum(1 for j in self.jobs if j.status == JobStatus.ERROR)

    @property
    def cancelled(self) -> int:
        return sum(1 for j in self.jobs if j.status == JobStatus.CANCELLED)

    @property
    def total_source_bytes(self) -> int:
        return sum(j.source_size_bytes for j in self.jobs)

    @property
    def total_output_bytes(self) -> int:
        return sum(j.output_size_bytes for j in self.jobs if j.status == JobStatus.DONE)

    @property
    def total_saved_bytes(self) -> int:
        return sum(j.size_saved_bytes for j in self.jobs)
