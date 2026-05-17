"""
Panel historii konwersji – lista poprzednich sesji.
"""
from __future__ import annotations

from tkinter import ttk

import customtkinter as ctk

from app.services.persistence import get_history
from app.utils.helpers import format_bytes

C_BG = "#0f1117"
C_BG2 = "#181c27"
C_BG3 = "#1e2233"
C_BORDER = "#2a3050"
C_ACCENT = "#4f8ef7"
C_RED = "#ef4444"
C_TEXT = "#e2e8f0"
C_TEXT_DIM = "#64748b"


class HistoryPanel(ctk.CTkFrame):
    COLUMNS = ("Data", "Źródło", "Pliki", "Tryb", "Zaoszczędzono", "Błędy")
    COL_WIDTHS = (130, 200, 60, 90, 110, 60)

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, fg_color=C_BG, corner_radius=0, **kwargs)
        self._build()
        self.refresh()

    def _build(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Pasek narzędzi
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        ctk.CTkLabel(
            toolbar,
            text="Historia konwersji",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=C_TEXT,
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="Wyczyść historię",
            command=self._clear_history,
            font=ctk.CTkFont(size=11),
            fg_color=C_BG3,
            hover_color=C_RED,
            text_color=C_TEXT,
            height=28,
            width=140,
            corner_radius=6,
        ).pack(side="right")

        # Treeview
        style = ttk.Style()
        style.configure(
            "History.Treeview",
            background=C_BG2,
            foreground=C_TEXT,
            fieldbackground=C_BG2,
            rowheight=24,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.configure(
            "History.Treeview.Heading",
            background=C_BG3,
            foreground=C_ACCENT,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "History.Treeview",
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
            style="History.Treeview",
            selectmode="browse",
        )

        for col, width in zip(self.COLUMNS, self.COL_WIDTHS):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=width, minwidth=50)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self._empty_label = ctk.CTkLabel(
            self,
            text="Brak historii konwersji",
            font=ctk.CTkFont(size=12),
            text_color=C_TEXT_DIM,
        )

    def refresh(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)

        entries = get_history().entries
        if not entries:
            self._empty_label.grid(row=2, column=0, pady=20)
            return
        else:
            self._empty_label.grid_forget()

        for e in entries:
            saved = format_bytes(e.total_saved_bytes)
            pct = f"{e.percent_saved:.1f}%"
            mode_short = "Lossless" if e.mode == "lossless" else f"Lossy/{e.quality_preset}"
            self._tree.insert(
                "",
                "end",
                values=(
                    e.timestamp_friendly,
                    e.source_path[:35] + "..." if len(e.source_path) > 35 else e.source_path,
                    f"{e.done_files}/{e.total_files}",
                    mode_short,
                    f"{saved} ({pct})",
                    e.error_files,
                ),
            )

    def _clear_history(self) -> None:
        get_history().clear()
        self.refresh()
