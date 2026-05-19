"""
Główne okno aplikacji WebP Forge.
Używa CustomTkinter z ciemnym motywem.
"""
from __future__ import annotations

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional

import customtkinter as ctk

from app.config.constants import (
    APP_NAME,
    APP_VERSION,
    CONVERSION_MODE_LABELS,
    FILENAME_LABELS,
    QUALITY_PRESETS,
)
from app.controllers.conversion_controller import ConversionController
from app.models.conversion_job import ConversionJob, ConversionResult, JobStatus
from app.services.persistence import get_settings
from app.utils.helpers import format_bytes, format_timestamp, run_in_main_thread
from app.views.conflict_dialog import ConflictDialog
from app.views.history_panel import HistoryPanel
from app.views.report_panel import ReportPanel

logger = logging.getLogger(__name__)

# ── stałe kolorów ─────────────────────────────────────────────────────────────
C_BG = "#0f1117"
C_BG2 = "#181c27"
C_BG3 = "#1e2233"
C_CARD = "#1a1f2e"
C_BORDER = "#2a3050"
C_ACCENT = "#4f8ef7"
C_ACCENT2 = "#7c3aed"
C_GREEN = "#22c55e"
C_RED = "#ef4444"
C_YELLOW = "#f59e0b"
C_TEXT = "#e2e8f0"
C_TEXT_DIM = "#64748b"
C_PROG_BG = "#1e2233"


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._settings = get_settings()
        self._controller = ConversionController()
        self._source_paths: List[Path] = []
        self._output_path: Optional[Path] = (
            Path(self._settings.last_output_path)
            if self._settings.last_output_path
            else None
        )
        self._conflict_result: Optional[str] = None
        self._conflict_event = threading.Event()

        self._setup_window()
        self._build_ui()
        self._wire_controller()
        self._restore_settings()

    # ── okno ──────────────────────────────────────────────────────────────────

    def _setup_window(self) -> None:
        w = self._settings.window_width
        h = self._settings.window_height
        self.title(f"{APP_NAME}  v{APP_VERSION}")
        self.geometry(f"{w}x{h}")
        self.minsize(900, 680)
        self.configure(fg_color=C_BG)
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icons" / "app.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception:
            pass

    # ── budowanie UI ──────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_main_area()
        self._build_statusbar()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color=C_BG2, corner_radius=0, height=64)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # logo-bar (gradient-like via accent line)
        accent_bar = ctk.CTkFrame(header, fg_color=C_ACCENT, width=4, corner_radius=0)
        accent_bar.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        accent_bar.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text=APP_NAME,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=C_TEXT,
        ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            header,
            text="Konwerter PNG/JPG → WebP  ·  szybko, bezstratnie lub stratnie",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=C_TEXT_DIM,
        ).grid(row=0, column=2, sticky="e", padx=20)

    def _build_main_area(self) -> None:
        main = ctk.CTkFrame(self, fg_color=C_BG, corner_radius=0)
        main.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=0, minsize=320)
        main.grid_columnconfigure(1, weight=1)

        self._build_left_panel(main)
        self._build_right_panel(main)

    def _build_left_panel(self, parent) -> None:
        left = ctk.CTkScrollableFrame(
            parent, fg_color=C_BG2, corner_radius=0, width=320,
            scrollbar_button_color=C_BORDER, scrollbar_button_hover_color=C_ACCENT,
        )
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        # Sekcja: Źródła
        self._section_label(left, "📁  ŹRÓDŁA WEJŚCIOWE")
        self._build_source_section(left)

        # Sekcja: Wyjście
        self._section_label(left, "💾  KATALOG WYJŚCIOWY")
        self._build_output_section(left)

        # Sekcja: Ustawienia
        self._section_label(left, "⚙️  USTAWIENIA KONWERSJI")
        self._build_settings_section(left)

        # Przyciski akcji
        self._build_action_buttons(left)

    def _section_label(self, parent, text: str) -> None:
        frame = ctk.CTkFrame(parent, fg_color=C_BG3, corner_radius=6)
        frame.grid(sticky="ew", padx=12, pady=(14, 4))
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            frame,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=C_ACCENT,
            anchor="w",
        ).grid(sticky="ew", padx=10, pady=6)

    def _card(self, parent, **kwargs) -> ctk.CTkFrame:
        defaults = dict(fg_color=C_CARD, corner_radius=8, border_width=1, border_color=C_BORDER)
        defaults.update(kwargs)
        f = ctk.CTkFrame(parent, **defaults)
        f.grid(sticky="ew", padx=12, pady=4)
        f.grid_columnconfigure(0, weight=1)
        return f

    def _build_source_section(self, parent) -> None:
        card = self._card(parent)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(sticky="ew", padx=8, pady=(8, 4))
        btn_row.grid_columnconfigure((0, 1, 2), weight=1)

        btn_style = dict(
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            hover_color=C_ACCENT,
            text_color=C_TEXT,
            height=32,
            corner_radius=6,
        )
        ctk.CTkButton(btn_row, text="Plik", command=self._pick_file, **btn_style).grid(
            row=0, column=0, padx=2, sticky="ew"
        )
        ctk.CTkButton(btn_row, text="Pliki", command=self._pick_files, **btn_style).grid(
            row=0, column=1, padx=2, sticky="ew"
        )
        ctk.CTkButton(btn_row, text="Folder", command=self._pick_folder, **btn_style).grid(
            row=0, column=2, padx=2, sticky="ew"
        )

        self._sources_label = ctk.CTkLabel(
            card,
            text="Brak wybranych plików",
            font=ctk.CTkFont(size=11),
            text_color=C_TEXT_DIM,
            anchor="w",
            wraplength=260,
        )
        self._sources_label.grid(sticky="ew", padx=10, pady=(0, 8))

    def _build_output_section(self, parent) -> None:
        card = self._card(parent)

        ctk.CTkButton(
            card,
            text="Wybierz katalog wyjściowy",
            command=self._pick_output,
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            hover_color=C_ACCENT,
            text_color=C_TEXT,
            height=32,
            corner_radius=6,
        ).grid(sticky="ew", padx=8, pady=(8, 4))

        self._output_label = ctk.CTkLabel(
            card,
            text="Nie wybrano",
            font=ctk.CTkFont(size=11),
            text_color=C_TEXT_DIM,
            anchor="w",
            wraplength=260,
        )
        self._output_label.grid(sticky="ew", padx=10, pady=(0, 8))

    def _build_settings_section(self, parent) -> None:
        card = self._card(parent)
        card.grid_columnconfigure(1, weight=1)

        # Tryb konwersji
        ctk.CTkLabel(card, text="Tryb:", font=ctk.CTkFont(size=11), text_color=C_TEXT_DIM, anchor="w").grid(
            row=0, column=0, sticky="w", padx=(10, 4), pady=(10, 2)
        )
        mode_values = list(CONVERSION_MODE_LABELS.values())
        self._mode_var = ctk.StringVar(value=mode_values[1])  # domyślnie Lossy
        self._mode_combo = ctk.CTkComboBox(
            card,
            values=mode_values,
            variable=self._mode_var,
            command=self._on_mode_change,
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            border_color=C_BORDER,
            button_color=C_ACCENT,
            dropdown_fg_color=C_BG3,
            text_color=C_TEXT,
            height=30,
        )
        self._mode_combo.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(10, 2))

        # Jakość
        self._quality_label_widget = ctk.CTkLabel(
            card, text="Jakość:", font=ctk.CTkFont(size=11), text_color=C_TEXT_DIM, anchor="w"
        )
        self._quality_label_widget.grid(row=1, column=0, sticky="w", padx=(10, 4), pady=2)
        quality_values = list(QUALITY_PRESETS.keys())
        self._quality_var = ctk.StringVar(value=self._settings.quality_preset)
        self._quality_combo = ctk.CTkComboBox(
            card,
            values=quality_values,
            variable=self._quality_var,
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            border_color=C_BORDER,
            button_color=C_ACCENT,
            dropdown_fg_color=C_BG3,
            text_color=C_TEXT,
            height=30,
            state="normal",
        )
        self._quality_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=2)

        # Nazwy plików
        ctk.CTkLabel(card, text="Nazwy:", font=ctk.CTkFont(size=11), text_color=C_TEXT_DIM, anchor="w").grid(
            row=2, column=0, sticky="w", padx=(10, 4), pady=(2, 10)
        )
        fname_values = list(FILENAME_LABELS.values())
        self._fname_var = ctk.StringVar(value=FILENAME_LABELS.get(self._settings.filename_behavior, fname_values[0]))
        ctk.CTkComboBox(
            card,
            values=fname_values,
            variable=self._fname_var,
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            border_color=C_BORDER,
            button_color=C_ACCENT,
            dropdown_fg_color=C_BG3,
            text_color=C_TEXT,
            height=30,
        ).grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=(2, 10))

    def _build_action_buttons(self, parent) -> None:
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(sticky="ew", padx=12, pady=(16, 12))
        frame.grid_columnconfigure((0, 1), weight=1)

        self._start_btn = ctk.CTkButton(
            frame,
            text="▶  Konwertuj",
            command=self._on_start,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=C_ACCENT,
            hover_color="#3b6fd4",
            text_color="white",
            height=42,
            corner_radius=8,
        )
        self._start_btn.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self._cancel_btn = ctk.CTkButton(
            frame,
            text="⛔  Anuluj",
            command=self._on_cancel,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=C_BG3,
            hover_color=C_RED,
            text_color=C_TEXT,
            height=42,
            corner_radius=8,
            state="disabled",
        )
        self._cancel_btn.grid(row=0, column=1, padx=(4, 0), sticky="ew")

    def _build_right_panel(self, parent) -> None:
        right = ctk.CTkFrame(parent, fg_color=C_BG, corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(2, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self._build_progress_area(right)
        self._build_tabview(right)

    def _build_progress_area(self, parent) -> None:
        pframe = ctk.CTkFrame(parent, fg_color=C_BG2, corner_radius=0, height=110)
        pframe.grid(row=0, column=0, sticky="ew")
        pframe.grid_propagate(False)
        pframe.grid_columnconfigure(0, weight=1)

        # Nagłówek statusu
        status_row = ctk.CTkFrame(pframe, fg_color="transparent")
        status_row.grid(sticky="ew", padx=16, pady=(10, 2))
        status_row.grid_columnconfigure(1, weight=1)

        self._status_icon = ctk.CTkLabel(
            status_row, text="⬜", font=ctk.CTkFont(size=16), text_color=C_TEXT_DIM
        )
        self._status_icon.grid(row=0, column=0, padx=(0, 8))

        self._status_label = ctk.CTkLabel(
            status_row,
            text="Gotowy do konwersji",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=C_TEXT,
            anchor="w",
        )
        self._status_label.grid(row=0, column=1, sticky="ew")

        self._counter_label = ctk.CTkLabel(
            status_row,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=C_TEXT_DIM,
        )
        self._counter_label.grid(row=0, column=2, padx=(8, 0))

        # Pasek postępu
        self._progress_bar = ctk.CTkProgressBar(
            pframe,
            mode="determinate",
            fg_color=C_BG3,
            progress_color=C_ACCENT,
            height=8,
            corner_radius=4,
        )
        self._progress_bar.set(0)
        self._progress_bar.grid(sticky="ew", padx=16, pady=(4, 4))

        # Plik bieżący
        self._file_label = ctk.CTkLabel(
            pframe,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=C_TEXT_DIM,
            anchor="w",
        )
        self._file_label.grid(sticky="ew", padx=16, pady=(0, 8))

    def _build_tabview(self, parent) -> None:
        tabview = ctk.CTkTabview(
            parent,
            fg_color=C_BG,
            segmented_button_fg_color=C_BG2,
            segmented_button_selected_color=C_ACCENT,
            segmented_button_selected_hover_color="#3b6fd4",
            segmented_button_unselected_color=C_BG2,
            segmented_button_unselected_hover_color=C_BG3,
            text_color=C_TEXT,
            border_width=0,
        )
        tabview.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)

        tabview.add("📋 Log operacji")
        tabview.add("📊 Raport")
        tabview.add("🕒 Historia")

        # Log
        self._log_text = ctk.CTkTextbox(
            tabview.tab("📋 Log operacji"),
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=C_BG2,
            text_color=C_TEXT,
            border_width=0,
            wrap="word",
        )
        self._log_text.pack(fill="both", expand=True, padx=4, pady=4)
        self._log_text.configure(state="disabled")

        # Raport
        self._report_panel = ReportPanel(tabview.tab("📊 Raport"))
        self._report_panel.pack(fill="both", expand=True)

        # Historia
        self._history_panel = HistoryPanel(tabview.tab("🕒 Historia"))
        self._history_panel.pack(fill="both", expand=True)

    def _build_statusbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=C_BG3, corner_radius=0, height=24)
        bar.grid(row=2, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            bar,
            text=f" {APP_NAME} v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=C_TEXT_DIM,
        ).grid(row=0, column=0, sticky="w")

        self._sb_right = ctk.CTkLabel(
            bar,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=C_TEXT_DIM,
        )
        self._sb_right.grid(row=0, column=2, sticky="e", padx=8)

    # ── okablowanie kontrolera ─────────────────────────────────────────────────

    def _wire_controller(self) -> None:
        self._controller.on_progress = self._on_progress
        self._controller.on_log = self._on_log
        self._controller.on_conflict = self._on_conflict_threadsafe
        self._controller.on_done = self._on_done
        self._controller.on_cancelled = self._on_cancelled

    # ── obsługa zdarzeń UI ─────────────────────────────────────────────────────

    def _pick_file(self) -> None:
        init = self._settings.last_input_path or str(Path.home())
        path = filedialog.askopenfilename(
            title="Wybierz plik PNG lub JPG",
            initialdir=init,
            filetypes=[
                ("Obrazy (PNG, JPG)", "*.png *.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("JPG / JPEG", "*.jpg *.jpeg"),
                ("Wszystkie pliki", "*.*"),
            ],
        )
        if path:
            self._set_sources([Path(path)])
            self._settings.last_input_path = str(Path(path).parent)

    def _pick_files(self) -> None:
        init = self._settings.last_input_path or str(Path.home())
        paths = filedialog.askopenfilenames(
            title="Wybierz pliki PNG lub JPG",
            initialdir=init,
            filetypes=[
                ("Obrazy (PNG, JPG)", "*.png *.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("JPG / JPEG", "*.jpg *.jpeg"),
                ("Wszystkie pliki", "*.*"),
            ],
        )
        if paths:
            self._set_sources([Path(p) for p in paths])
            self._settings.last_input_path = str(Path(paths[0]).parent)

    def _pick_folder(self) -> None:
        init = self._settings.last_input_path or str(Path.home())
        path = filedialog.askdirectory(title="Wybierz folder z plikami PNG/JPG", initialdir=init)
        if path:
            self._set_sources([Path(path)])
            self._settings.last_input_path = path

    def _pick_output(self) -> None:
        init = self._settings.last_output_path or str(Path.home())
        path = filedialog.askdirectory(title="Wybierz katalog wyjściowy", initialdir=init)
        if path:
            self._output_path = Path(path)
            self._settings.last_output_path = path
            self._output_label.configure(text=path, text_color=C_TEXT)

    def _set_sources(self, paths: List[Path]) -> None:
        self._source_paths = paths
        if len(paths) == 1:
            label = str(paths[0])
        else:
            label = f"{len(paths)} plików"
        self._sources_label.configure(text=label, text_color=C_TEXT)

    def _on_mode_change(self, value: str) -> None:
        from app.config.constants import CONVERSION_MODE_LOSSLESS, CONVERSION_MODE_LABELS
        is_lossless = value == CONVERSION_MODE_LABELS[CONVERSION_MODE_LOSSLESS]
        state = "disabled" if is_lossless else "normal"
        self._quality_combo.configure(state=state)
        self._quality_label_widget.configure(
            text_color=C_TEXT_DIM if is_lossless else C_TEXT_DIM
        )

    def _on_start(self) -> None:
        if self._controller.is_running:
            return

        if not self._source_paths:
            messagebox.showwarning("Brak źródeł", "Wybierz co najmniej jeden plik lub folder PNG/JPG.")
            return
        if not self._output_path:
            messagebox.showwarning("Brak celu", "Wybierz katalog wyjściowy.")
            return

        # Odczyt ustawień z GUI
        mode_label = self._mode_var.get()
        mode = next(
            (k for k, v in CONVERSION_MODE_LABELS.items() if v == mode_label),
            "lossy",
        )
        quality_preset = self._quality_var.get()
        fname_label = self._fname_var.get()
        fname_behavior = next(
            (k for k, v in FILENAME_LABELS.items() if v == fname_label),
            "keep",
        )

        # Zapis ustawień
        self._settings.update({
            "conversion_mode": mode,
            "quality_preset": quality_preset,
            "filename_behavior": fname_behavior,
        })

        # Reset UI
        self._progress_bar.set(0)
        self._status_label.configure(text="Trwa konwersja...", text_color=C_YELLOW)
        self._status_icon.configure(text="🔄")
        self._counter_label.configure(text="")
        self._file_label.configure(text="")
        self._start_btn.configure(state="disabled")
        self._cancel_btn.configure(state="normal")
        self._report_panel.clear()
        self._append_log(f"[{format_timestamp()}] 🚀 Rozpoczęcie konwersji ({mode}, {quality_preset})")

        self._controller.start_conversion(
            sources=self._source_paths,
            output_root=self._output_path,
            mode=mode,
            quality_preset=quality_preset,
            filename_behavior=fname_behavior,
        )

    def _on_cancel(self) -> None:
        self._controller.cancel()
        self._cancel_btn.configure(state="disabled")

    # ── callbacki kontrolera ───────────────────────────────────────────────────

    def _on_progress(self, current: int, total: int, job: ConversionJob) -> None:
        """Wywoływany z wątku roboczego – planuje aktualizację GUI."""
        run_in_main_thread(self, self._update_progress_ui, current, total, job)

    def _update_progress_ui(self, current: int, total: int, job: ConversionJob) -> None:
        pct = current / total if total else 0
        self._progress_bar.set(pct)
        self._counter_label.configure(text=f"{current}/{total}")
        self._file_label.configure(text=str(job.source_path.name))

        status_icons = {
            JobStatus.DONE: "✓",
            JobStatus.ERROR: "✗",
            JobStatus.SKIPPED: "⏭",
            JobStatus.CANCELLED: "⛔",
        }
        icon = status_icons.get(job.status, "🔄")
        self._status_label.configure(text=f"{icon}  {job.source_path.name}")

        # Aktualizuj raport
        self._report_panel.add_job(job)

    def _on_log(self, message: str) -> None:
        run_in_main_thread(self, self._append_log, message)

    def _append_log(self, message: str) -> None:
        self._log_text.configure(state="normal")
        self._log_text.insert("end", message + "\n")
        self._log_text.see("end")
        self._log_text.configure(state="disabled")
        # Przycinaj log do max linii
        lines = int(self._log_text.index("end-1c").split(".")[0])
        from app.config.constants import LOG_MAX_LINES
        if lines > LOG_MAX_LINES:
            self._log_text.configure(state="normal")
            self._log_text.delete("1.0", f"{lines - LOG_MAX_LINES}.0")
            self._log_text.configure(state="disabled")

    def _on_conflict_threadsafe(self, job: ConversionJob) -> str:
        """
        Wywoływany z wątku roboczego.
        Planuje otwarcie dialogu w main thread i blokuje wątek roboczy do decyzji.
        """
        self._conflict_event.clear()
        self._conflict_result = None
        run_in_main_thread(self, self._show_conflict_dialog, job)
        self._conflict_event.wait(timeout=300)
        return self._conflict_result or "skip"

    def _show_conflict_dialog(self, job: ConversionJob) -> None:
        dialog = ConflictDialog(self, job)
        result = dialog.get_result()
        self._conflict_result = result
        self._conflict_event.set()

    def _on_done(self, result: ConversionResult) -> None:
        run_in_main_thread(self, self._finalize_ui, result, False)

    def _on_cancelled(self, result: ConversionResult) -> None:
        run_in_main_thread(self, self._finalize_ui, result, True)

    def _finalize_ui(self, result: ConversionResult, cancelled: bool) -> None:
        self._start_btn.configure(state="normal")
        self._cancel_btn.configure(state="disabled")
        self._progress_bar.set(1.0 if not cancelled else self._progress_bar.get())

        saved = format_bytes(result.total_saved_bytes)
        if cancelled:
            self._status_label.configure(text=f"Anulowano – zapisano {saved}", text_color=C_RED)
            self._status_icon.configure(text="⛔")
        else:
            self._status_label.configure(
                text=f"✅  Gotowe! {result.done}/{result.total} plików · zaoszczędzono {saved}",
                text_color=C_GREEN,
            )
            self._status_icon.configure(text="✅")

        self._sb_right.configure(
            text=f"Ostatnia sesja: {result.done} ok · {result.errors} błędów · {result.skipped} pominięto"
        )

        # Odśwież historię
        self._history_panel.refresh()

    # ── przywracanie ustawień ──────────────────────────────────────────────────

    def _restore_settings(self) -> None:
        # Tryb
        mode_label = CONVERSION_MODE_LABELS.get(self._settings.conversion_mode, list(CONVERSION_MODE_LABELS.values())[1])
        self._mode_var.set(mode_label)
        self._on_mode_change(mode_label)

        # Jakość
        self._quality_var.set(self._settings.quality_preset)

        # Wyjście
        if self._output_path:
            self._output_label.configure(text=str(self._output_path), text_color=C_TEXT)

    def on_close(self) -> None:
        try:
            self._settings.update({
                "window_width": self.winfo_width(),
                "window_height": self.winfo_height(),
            })
        except Exception:
            pass
        self.destroy()
