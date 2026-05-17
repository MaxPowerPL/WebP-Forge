"""
Panel raportu – tabela z wynikami konwersji plików.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List

import customtkinter as ctk

from app.models.conversion_job import ConversionJob, JobStatus
from app.utils.helpers import format_bytes

C_BG = "#0f1117"
C_BG2 = "#181c27"
C_BG3 = "#1e2233"
C_BORDER = "#2a3050"
C_ACCENT = "#4f8ef7"
C_GREEN = "#22c55e"
C_RED = "#ef4444"
C_YELLOW = "#f59e0b"
C_TEXT = "#e2e8f0"
C_TEXT_DIM = "#64748b"


class ReportPanel(ctk.CTkFrame):
    COLUMNS = ("Plik", "Rozmiar PNG", "Rozmiar WebP", "Zaoszczędzono", "Status")
    COL_WIDTHS = (200, 100, 100, 110, 80)

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, fg_color=C_BG, corner_radius=0, **kwargs)
        self._rows: List[dict] = []
        self._build()

    def _build(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Nagłówek z podsumowaniem
        self._summary_label = ctk.CTkLabel(
            self,
            text="Brak danych – uruchom konwersję",
            font=ctk.CTkFont(size=11),
            text_color=C_TEXT_DIM,
            anchor="w",
        )
        self._summary_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 4))

        # Treeview ze stylem
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "WebPForge.Treeview",
            background=C_BG2,
            foreground=C_TEXT,
            fieldbackground=C_BG2,
            rowheight=24,
            font=("Consolas", 10),
            borderwidth=0,
        )
        style.configure(
            "WebPForge.Treeview.Heading",
            background=C_BG3,
            foreground=C_ACCENT,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "WebPForge.Treeview",
            background=[("selected", C_ACCENT)],
            foreground=[("selected", "white")],
        )

        tree_frame = ctk.CTkFrame(self, fg_color=C_BG2, corner_radius=6, border_width=1, border_color=C_BORDER)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(
            tree_frame,
            columns=self.COLUMNS,
            show="headings",
            style="WebPForge.Treeview",
            selectmode="browse",
        )

        for col, width in zip(self.COLUMNS, self.COL_WIDTHS):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=width, minwidth=60)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)

        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # tagi koloru wierszy
        self._tree.tag_configure("done", foreground=C_GREEN)
        self._tree.tag_configure("error", foreground=C_RED)
        self._tree.tag_configure("skipped", foreground=C_YELLOW)
        self._tree.tag_configure("cancelled", foreground=C_TEXT_DIM)

    def clear(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._rows.clear()
        self._summary_label.configure(text="")

    def add_job(self, job: ConversionJob) -> None:
        tag_map = {
            JobStatus.DONE: "done",
            JobStatus.ERROR: "error",
            JobStatus.SKIPPED: "skipped",
            JobStatus.CANCELLED: "cancelled",
        }
        status_labels = {
            JobStatus.DONE: "✓ OK",
            JobStatus.ERROR: "✗ Błąd",
            JobStatus.SKIPPED: "⏭ Pominięto",
            JobStatus.CANCELLED: "⛔ Anulowano",
        }

        tag = tag_map.get(job.status, "done")
        status_text = status_labels.get(job.status, "?")

        src_size = format_bytes(job.source_size_bytes) if job.source_size_bytes else "-"
        out_size = format_bytes(job.output_size_bytes) if job.output_size_bytes else "-"
        saved = f"{job.percent_saved:.1f}%" if job.status == JobStatus.DONE else "-"

        # Sprawdź czy wiersz dla tego pliku już istnieje
        for item_id in self._tree.get_children():
            vals = self._tree.item(item_id, "values")
            if vals and vals[0] == job.source_path.name:
                self._tree.item(
                    item_id,
                    values=(job.source_path.name, src_size, out_size, saved, status_text),
                    tags=(tag,),
                )
                return

        self._tree.insert(
            "",
            "end",
            values=(job.source_path.name, src_size, out_size, saved, status_text),
            tags=(tag,),
        )
        self._tree.yview_moveto(1.0)

    def update_summary(self, done: int, total: int, saved_bytes: int) -> None:
        self._summary_label.configure(
            text=f"Przetworzone: {done}/{total}  ·  Zaoszczędzono łącznie: {format_bytes(saved_bytes)}",
            text_color=C_TEXT,
        )
