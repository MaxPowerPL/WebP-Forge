"""
Kontroler konwersji – orkiestruje cały pipeline:
skanowanie → budowanie zadań → wielowątkowa konwersja → raportowanie.

GUI komunikuje się przez callbacki, więc kontroler jest niezależny od widoku.
"""
from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional

from app.config.constants import (
    MAX_WORKER_THREADS,
    QUALITY_PRESETS,
    CONFLICT_OVERWRITE,
    CONFLICT_SKIP,
    CONFLICT_SUFFIX,
)
from app.models.conversion_job import ConversionJob, ConversionResult, JobStatus
from app.models.history import HistoryEntry
from app.services.converter import convert_png_to_webp
from app.services.persistence import get_history, get_settings
from app.services.scanner import (
    apply_suffix_to_avoid_conflict,
    resolve_output_path,
    scan_png_files,
)
from app.utils.helpers import CancelToken, format_timestamp

logger = logging.getLogger(__name__)


class ConversionController:
    """
    Centralna klasa zarządzająca konwersją.

    Callbacki GUI (wszystkie opcjonalne):
        on_progress(current: int, total: int, job: ConversionJob)
        on_log(message: str)
        on_conflict(job: ConversionJob) -> str  # musi zwrócić 'overwrite'|'skip'|'suffix'
        on_done(result: ConversionResult)
        on_cancelled(result: ConversionResult)
    """

    def __init__(self) -> None:
        self._cancel_token = CancelToken()
        self._lock = threading.Lock()
        self._running = False

        # callbacki (ustawiane przez widok przez kontroler główny)
        self.on_progress: Optional[Callable] = None
        self.on_log: Optional[Callable] = None
        self.on_conflict: Optional[Callable] = None
        self.on_done: Optional[Callable] = None
        self.on_cancelled: Optional[Callable] = None

    # ── public API ─────────────────────────────────────────────────────────────

    @property
    def is_running(self) -> bool:
        return self._running

    def cancel(self) -> None:
        self._cancel_token.cancel()
        self._log("⛔ Anulowanie – czekam na zakończenie bieżących zadań...")

    def start_conversion(
        self,
        sources: List[Path],
        output_root: Path,
        mode: str,
        quality_preset: str,
        filename_behavior: str,
    ) -> None:
        """Uruchamia konwersję w tle (nie blokuje GUI)."""
        if self._running:
            return
        self._cancel_token.reset()
        thread = threading.Thread(
            target=self._run,
            args=(sources, output_root, mode, quality_preset, filename_behavior),
            daemon=True,
        )
        thread.start()

    # ── private ────────────────────────────────────────────────────────────────

    def _run(
        self,
        sources: List[Path],
        output_root: Path,
        mode: str,
        quality_preset: str,
        filename_behavior: str,
    ) -> None:
        self._running = True
        quality = QUALITY_PRESETS.get(quality_preset, 82)
        result = ConversionResult()

        try:
            # 1. Skanowanie
            self._log("🔍 Skanowanie plików PNG...")
            all_files: List[Path] = []
            source_roots: dict[Path, Path] = {}

            for source in sources:
                files = scan_png_files(source)
                for f in files:
                    all_files.append(f)
                    root = source if source.is_dir() else source.parent
                    source_roots[f] = root

            if not all_files:
                self._log("⚠️ Nie znaleziono żadnych plików PNG.")
                self._running = False
                return

            self._log(f"📂 Znaleziono {len(all_files)} plików PNG.")

            # 2. Budowanie zadań
            jobs: List[ConversionJob] = []
            for f in all_files:
                out = resolve_output_path(
                    f, source_roots[f], output_root, filename_behavior
                )
                jobs.append(
                    ConversionJob(
                        source_path=f,
                        output_path=out,
                        mode=mode,
                        quality=quality,
                        filename_behavior=filename_behavior,
                    )
                )
            result.jobs = jobs

            # 3. Konwersja
            total = len(jobs)
            done_count = 0

            # Używamy jednego wątku per zadanie, ale serializujemy obsługę konfliktów
            # w głównym wątku przez callback on_conflict (blokujący dialog).
            with ThreadPoolExecutor(max_workers=MAX_WORKER_THREADS) as executor:
                future_to_job = {}
                for job in jobs:
                    if self._cancel_token.is_cancelled:
                        job.status = JobStatus.CANCELLED
                        continue

                    # Obsługa konfliktu PRZED zleceniem do puli
                    if job.output_path.exists():
                        resolution = self._resolve_conflict(job)
                        if resolution == CONFLICT_SKIP:
                            job.status = JobStatus.SKIPPED
                            done_count += 1
                            self._emit_progress(done_count, total, job)
                            self._log(f"⏭ Pominięto: {job.source_path.name}")
                            continue
                        elif resolution == CONFLICT_SUFFIX:
                            job.output_path = apply_suffix_to_avoid_conflict(job.output_path)

                    future = executor.submit(convert_png_to_webp, job)
                    future_to_job[future] = job

                for future in as_completed(future_to_job):
                    job = future_to_job[future]
                    if self._cancel_token.is_cancelled:
                        job.status = JobStatus.CANCELLED
                        done_count += 1
                        self._emit_progress(done_count, total, job)
                        continue

                    try:
                        future.result()
                    except Exception as exc:
                        job.status = JobStatus.ERROR
                        job.error_message = str(exc)

                    done_count += 1
                    self._emit_progress(done_count, total, job)
                    self._log_job(job)

            # Anuluj pozostałe (jeszcze PENDING)
            for job in result.jobs:
                if job.status == JobStatus.PENDING:
                    job.status = JobStatus.CANCELLED

        finally:
            self._running = False
            self._save_history(result, sources, output_root, mode, quality_preset)

            if self._cancel_token.is_cancelled:
                self._log(f"🚫 Anulowano. Przetworzono {result.done}/{result.total}.")
                if self.on_cancelled:
                    self.on_cancelled(result)
            else:
                self._log(
                    f"✅ Zakończono! Przetworzone: {result.done}, "
                    f"Pominięte: {result.skipped}, Błędy: {result.errors}"
                )
                if self.on_done:
                    self.on_done(result)

    def _resolve_conflict(self, job: ConversionJob) -> str:
        """Pyta GUI o decyzję (blokująco). Fallback: nadpisz."""
        if self.on_conflict:
            # on_conflict jest wywoływany z wątku roboczego – dialog musi być
            # thread-safe (CustomTkinter wymaga wywołania z main thread).
            # Implementacja w widoku używa threading.Event do synchronizacji.
            return self.on_conflict(job)
        return CONFLICT_OVERWRITE

    def _emit_progress(self, current: int, total: int, job: ConversionJob) -> None:
        if self.on_progress:
            try:
                self.on_progress(current, total, job)
            except Exception:
                pass

    def _log(self, message: str) -> None:
        ts = format_timestamp()
        full = f"[{ts}] {message}"
        logger.info(message)
        if self.on_log:
            try:
                self.on_log(full)
            except Exception:
                pass

    def _log_job(self, job: ConversionJob) -> None:
        name = job.source_path.name
        if job.status == JobStatus.DONE:
            pct = job.percent_saved
            self._log(f"✓ {name}  →  zaoszczędzono {pct:.1f}%")
        elif job.status == JobStatus.ERROR:
            self._log(f"✗ {name}  –  błąd: {job.error_message}")
        elif job.status == JobStatus.SKIPPED:
            self._log(f"⏭ {name}  –  pominięto")
        elif job.status == JobStatus.CANCELLED:
            self._log(f"⛔ {name}  –  anulowano")

    def _save_history(
        self,
        result: ConversionResult,
        sources: List[Path],
        output_root: Path,
        mode: str,
        quality_preset: str,
    ) -> None:
        try:
            src_str = "; ".join(str(s) for s in sources)
            entry = HistoryEntry(
                timestamp=format_timestamp(),
                source_path=src_str,
                output_path=str(output_root),
                total_files=result.total,
                done_files=result.done,
                skipped_files=result.skipped,
                error_files=result.errors,
                mode=mode,
                quality_preset=quality_preset,
                total_saved_bytes=result.total_saved_bytes,
                total_source_bytes=result.total_source_bytes,
            )
            get_history().add(entry)
        except Exception as exc:
            logger.error("Nie można zapisać historii: %s", exc)
