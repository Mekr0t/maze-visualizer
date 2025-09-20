"""
Main application window.

Orchestrates:
  - parameter controls
  - canvas rendering
  - cooperative cancellation
  - adaptive batching / delay
"""

from __future__ import annotations

__all__ = ["MazeApp"]

import tkinter as tk
from tkinter import messagebox
from typing import Any, Iterator

from gui.controls import Controls
from gui.grid_canvas import GridCanvas
from maze.generator import get_generator
from maze.maze import Maze
from maze.solver import get_solver
from utils.colors import PALETTE

# ------------------------------------------------------------------ #
# Animation tunables
# ------------------------------------------------------------------ #
_MIN_BATCH: int = 1
_MAX_BATCH_GEN: int = 50
_MAX_BATCH_SOLVE: int = 3
_DELAY_INSTANT: int = 0
_DELAY_MAX: int = 100  # ms


class MazeApp(tk.Tk):
    """Root window and animation scheduler."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Maze Generator & Solver")
        self.geometry("900x600")
        self.resizable(True, True)

        self.maze: Maze | None = None
        self.start: tuple[int, int] = (0, 0)
        self.goal: tuple[int, int] = (0, 0)

        # Cooperative cancellation
        self._after_id: str | None = None
        self._run_seq: int = 0
        self._kind: str | None = None  # "gen" | "solve"

        # Batching
        self._batch_size: int = _MIN_BATCH
        self._batch_cnt: int = 0

        self._build_widgets()
        self.bind("<Configure>", self._on_resize)

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #
    def _build_widgets(self) -> None:
        self.controls = Controls(self, on_generate=self.generate, on_solve=self.solve)
        self.controls.pack(side="left", fill="y", padx=6, pady=6)

        self.canvas = GridCanvas(self, bg=PALETTE.wall)
        self.canvas.pack(side="right", expand=True, fill="both")

    # ------------------------------------------------------------------ #
    # Cancellation
    # ------------------------------------------------------------------ #
    def _cancel(self) -> None:
        """Cancel any scheduled after() call and bump epoch."""
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None
        self._run_seq += 1
        self._kind = None
        self._batch_cnt = 0

    # ------------------------------------------------------------------ #
    # User actions
    # ------------------------------------------------------------------ #
    def generate(
        self, rows: int, cols: int, gen_name: str, speed_pct: float
    ) -> None:
        """Start maze generation."""
        self._cancel()
        self.maze = Maze(cols, rows)
        self._auto_scale()
        self.canvas.reset_path()
        self.canvas.draw_maze(self.maze)
        self.update_idletasks()

        delay, batch = self._calc_delay_batch(speed_pct, rows * cols, False)
        self._batch_size = batch
        gen = get_generator(gen_name)
        self._run_iterator(gen(self.maze.w, self.maze.h), delay, "gen")

    def solve(self, sol_name: str, speed_pct: float) -> None:
        """Start path finding."""
        if self.maze is None:
            messagebox.showwarning("No maze", "Generate a maze first")
            return
        if self._kind == "gen":
            messagebox.showinfo("Busy", "Wait until generation finishes")
            return

        self._cancel()
        solver = get_solver(sol_name)
        self._pick_endpoints()
        self.canvas.draw_markers(self.start, self.goal)
        self.canvas.reset_path()

        delay, batch = self._calc_delay_batch(speed_pct, self.maze.w * self.maze.h, True)
        self._batch_size = batch
        self._run_iterator(solver(self.maze, self.start, self.goal), delay, "solve")

    # ------------------------------------------------------------------ #
    # Animation engine
    # ------------------------------------------------------------------ #
    def _run_iterator(self, it: Iterator[Any], delay_ms: int, kind: str) -> None:
        """Schedule iterator with cooperative cancellation & batching."""
        self._kind = kind
        epoch = self._run_seq  # captured in closure

        def job() -> None:
            nonlocal epoch
            if epoch != self._run_seq:
                return  # stale job

            updates = 0
            try:
                while updates < self._batch_size:
                    if kind == "gen":
                        x, y, action = next(it)
                        self.maze.grid[y, x] = action
                        color = PALETTE.passage if action else PALETTE.wall
                        self.canvas.draw_cell(x, y, colour=color)
                    else:  # solve
                        path = next(it)
                        self.canvas.draw_path(path)

                    updates += 1

                # schedule next batch
                self._after_id = self.after(max(1, delay_ms), job)

            except StopIteration:
                # finished
                self._after_id = None
                if kind == "gen":
                    self._pick_endpoints()
                    self.canvas.draw_markers(self.start, self.goal)
                self.canvas.tag_raise("markers")
                self._kind = None

        self._after_id = self.after(1, job)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _calc_delay_batch(
        self, speed_pct: float, cell_count: int, solving: bool
    ) -> tuple[int, int]:
        """Return (delay_ms, batch_size) adapted to speed and maze size."""
        if speed_pct >= 100:
            return _DELAY_INSTANT, _MAX_BATCH_GEN

        delay = int(100 * (1 - (speed_pct - 1) / 99) ** 1.5)
        if solving:
            batch = min(_MAX_BATCH_SOLVE, max(_MIN_BATCH, cell_count // 400))
        else:
            batch = min(_MAX_BATCH_GEN, max(_MIN_BATCH, cell_count // 200))
        return max(1, delay), batch

    def _pick_endpoints(self) -> None:
        """Choose start/goal on passage cells."""
        def first_passage(search_from: tuple[int, int]) -> tuple[int, int]:
            x0, y0 = search_from
            for y in range(self.maze.h):
                for x in range(self.maze.w):
                    xx = x if x0 == 0 else self.maze.w - 1 - x
                    yy = y if y0 == 0 else self.maze.h - 1 - y
                    if self.maze.grid[yy, xx]:
                        return (xx, yy)
            return (x0, y0)

        self.start = first_passage((0, 0))
        self.goal = first_passage((self.maze.w - 1, self.maze.h - 1))

    def _on_resize(self, event: tk.Event) -> None:
        """Auto-scale cell size when window changes."""
        if event.widget is self and self.maze:
            self._auto_scale()

    def _auto_scale(self) -> None:
        """Compute optimal cell_px and redraw."""
        if not self.maze:
            return
        cw = self.canvas.winfo_width() - 20
        ch = self.canvas.winfo_height() - 20
        if cw <= 0 or ch <= 0:
            return
        optimal = max(4, min(cw // (self.maze.w + 2), ch // (self.maze.h + 2), 40))
        if abs(self.canvas.cell_px - optimal) > 1:
            self.canvas.cell_px = optimal
            self.canvas.draw_maze(self.maze)
            self.canvas.draw_markers(self.start, self.goal)


def main() -> None:
    """Entry-point for python -m gui.app"""
    MazeApp().mainloop()
