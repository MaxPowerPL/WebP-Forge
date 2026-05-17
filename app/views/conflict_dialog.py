"""
Dialog konfliktu pliku – blokujący, wywołany z głównego wątku.
"""
from __future__ import annotations

from typing import Optional

import customtkinter as ctk

from app.models.conversion_job import ConversionJob

C_BG = "#0f1117"
C_BG2 = "#181c27"
C_BG3 = "#1e2233"
C_CARD = "#1a1f2e"
C_BORDER = "#2a3050"
C_ACCENT = "#4f8ef7"
C_RED = "#ef4444"
C_YELLOW = "#f59e0b"
C_TEXT = "#e2e8f0"
C_TEXT_DIM = "#64748b"


class ConflictDialog(ctk.CTkToplevel):
    def __init__(self, parent, job: ConversionJob) -> None:
        super().__init__(parent)
        self._result: Optional[str] = None

        self.title("Konflikt pliku")
        self.geometry("480x280")
        self.resizable(False, False)
        self.configure(fg_color=C_BG2)
        self.grab_set()
        self.focus()

        # Wyśrodkuj względem rodzica
        self.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width() // 2 - 240
        py = parent.winfo_y() + parent.winfo_height() // 2 - 140
        self.geometry(f"+{px}+{py}")

        self._build(job)
        self.protocol("WM_DELETE_WINDOW", lambda: self._choose("skip"))

    def _build(self, job: ConversionJob) -> None:
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="⚠️  Konflikt – plik już istnieje",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=C_YELLOW,
        ).grid(pady=(18, 6), padx=20)

        ctk.CTkLabel(
            self,
            text="Plik docelowy:",
            font=ctk.CTkFont(size=11),
            text_color=C_TEXT_DIM,
        ).grid(sticky="w", padx=24)

        ctk.CTkLabel(
            self,
            text=str(job.output_path),
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=C_TEXT,
            wraplength=430,
            justify="left",
        ).grid(sticky="w", padx=24, pady=(0, 16))

        ctk.CTkLabel(
            self,
            text="Co zrobić z tym plikiem?",
            font=ctk.CTkFont(size=12),
            text_color=C_TEXT,
        ).grid(pady=(0, 10))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.grid(padx=16, pady=(0, 16))

        btn_style = dict(
            font=ctk.CTkFont(size=12, weight="bold"),
            height=38,
            corner_radius=8,
            width=130,
        )

        ctk.CTkButton(
            btn_row,
            text="Nadpisz",
            fg_color=C_RED,
            hover_color="#c53030",
            command=lambda: self._choose("overwrite"),
            **btn_style,
        ).grid(row=0, column=0, padx=4)

        ctk.CTkButton(
            btn_row,
            text="Pomiń",
            fg_color=C_BG3,
            hover_color=C_BORDER,
            command=lambda: self._choose("skip"),
            **btn_style,
        ).grid(row=0, column=1, padx=4)

        ctk.CTkButton(
            btn_row,
            text="Dodaj sufiks _1",
            fg_color=C_ACCENT,
            hover_color="#3b6fd4",
            command=lambda: self._choose("suffix"),
            **btn_style,
        ).grid(row=0, column=2, padx=4)

    def _choose(self, result: str) -> None:
        self._result = result
        self.grab_release()
        self.destroy()

    def get_result(self) -> str:
        self.wait_window()
        return self._result or "skip"
