"""
Control panel for the maze visualiser.

Provides:
  - rows / cols spinboxes
  - speed slider (1-100 %) with human label
  - generator & solver dropdowns
  - Generate / Solve buttons

All user choices are forwarded via two callbacks:
  on_generate(rows, cols, generator_name, speed_percent)
  on_solve(solver_name, speed_percent)
"""

from __future__ import annotations

__all__ = ["Controls"]

import tkinter as tk
from tkinter import ttk
from typing import Callable

from maze.generator import list_generators
from maze.solver import list_solvers

# ------------------------------------------------------------------ #
# Constants
# ------------------------------------------------------------------ #
_MIN_SIZE: int = 5
_MAX_SIZE: int = 200
_DEFAULT_ROWS: int = 25
_DEFAULT_COLS: int = 25
_DEFAULT_SPEED: int = 80  # percent

_SPEED_LABELS: dict[int, str] = {
    100: "Speed: Max",
    90: "Speed: {}% (Very Fast)",
    70: "Speed: {}% (Fast)",
    30: "Speed: {}% (Medium)",
    10: "Speed: {}% (Slow)",
}


class Controls(ttk.Frame):
    """Parameter panel embedded in the main window."""

    def __init__(
        self,
        parent: tk.Widget,
        *,
        on_generate: Callable[[int, int, str, float], None],
        on_solve: Callable[[str, float], None],
        **kwargs: object,
    ) -> None:
        """
        Args:
            parent: Parent widget.
            on_generate: Callback(rows, cols, generator_name, speed_percent).
            on_solve: Callback(solver_name, speed_percent).
        """
        super().__init__(parent, **kwargs)
        self.on_generate = on_generate
        self.on_solve = on_solve

        self._build()
        self._update_speed_label(_DEFAULT_SPEED)

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #
    def _build(self) -> None:
        """Create and grid all child widgets."""
        # Rows
        ttk.Label(self, text="Rows").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.rows_var = tk.IntVar(value=_DEFAULT_ROWS)
        ttk.Spinbox(
            self,
            from_=_MIN_SIZE,
            to=_MAX_SIZE,
            textvariable=self.rows_var,
            width=8,
        ).grid(row=0, column=1, sticky="ew", padx=5)

        # Cols
        ttk.Label(self, text="Cols").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.cols_var = tk.IntVar(value=_DEFAULT_COLS)
        ttk.Spinbox(
            self,
            from_=_MIN_SIZE,
            to=_MAX_SIZE,
            textvariable=self.cols_var,
            width=8,
        ).grid(row=1, column=1, sticky="ew", padx=5)

        # Auto-size info
        ttk.Label(self, text="Cell size: Auto").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2
        )

        # Speed slider
        self.speed_label = ttk.Label(self, text="")
        self.speed_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)

        self.speed_var = tk.DoubleVar(value=_DEFAULT_SPEED)
        ttk.Scale(
            self,
            from_=1,
            to=100,
            orient="horizontal",
            variable=self.speed_var,
            command=self._update_speed_label,
            length=200,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        # Generator choice
        ttk.Label(self, text="Generator").grid(
            row=5, column=0, sticky="w", padx=5, pady=(15, 2)
        )
        self.gen_combo = ttk.Combobox(
            self, values=list_generators(), state="readonly", width=18
        )
        self.gen_combo.current(0)
        self.gen_combo.grid(row=5, column=1, sticky="ew", padx=5)

        # Generate button
        ttk.Button(self, text="Generate", command=self._generate).grid(
            row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=8
        )

        # Solver choice
        ttk.Label(self, text="Solver").grid(
            row=7, column=0, sticky="w", padx=5, pady=(15, 2)
        )
        self.sol_combo = ttk.Combobox(
            self, values=list_solvers(), state="readonly", width=18
        )
        self.sol_combo.current(0)
        self.sol_combo.grid(row=7, column=1, sticky="ew", padx=5)

        # Solve button
        ttk.Button(self, text="Solve", command=self._solve).grid(
            row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=8
        )

        # Resize behaviour
        self.columnconfigure(1, weight=1)

    # ------------------------------------------------------------------ #
    # Event handlers
    # ------------------------------------------------------------------ #
    def _update_speed_label(self, value: str | float) -> None:
        """Translate slider float to human text."""
        percent = int(float(value))
        template = next(
            (t for threshold, t in _SPEED_LABELS.items() if percent >= threshold),
            "Speed: {}% (Very Slow)",
        )
        self.speed_label.config(text=template.format(percent))

    def _generate(self) -> None:
        """Fire user callback."""
        self.on_generate(
            self.rows_var.get(),
            self.cols_var.get(),
            self.gen_combo.get(),
            self.speed_var.get(),
        )

    def _solve(self) -> None:
        """Fire user callback."""
        self.on_solve(self.sol_combo.get(), self.speed_var.get())