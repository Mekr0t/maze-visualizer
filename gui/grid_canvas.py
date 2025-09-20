"""
Canvas specialised for drawing a rectangular maze and overlay paths.

Coordinates are (x,y) with origin at top-left.
The maze is rendered inside a 1-cell black border.
"""

from __future__ import annotations

__all__ = ["GridCanvas"]

import tkinter as tk
from typing import Iterable, Tuple

from maze.maze import Maze
from utils.colors import PALETTE

_Node = Tuple[int, int]


class GridCanvas(tk.Canvas):
    """Efficiently draws maze grid, path, visited cells, start/goal markers."""

    DEFAULT_CELL_PX: int = 12  # fallback if parent does not override

    def __init__(
        self,
        parent: tk.Widget,
        *,
        cell_px: int = DEFAULT_CELL_PX,
        **kwargs: object,
    ) -> None:
        """
        Args:
            parent: Parent widget.
            cell_px: Edge length of one cell in pixels.
        """
        super().__init__(parent, **kwargs)
        self.cell_px = cell_px
        self.maze: Maze | None = None

        # Overlay bookkeeping
        self._path_objects: dict[_Node, int] = {}  # (x,y) -> canvas id
        self._visited_objects: dict[_Node, int] = {}
        self._current_path: list[_Node] = []

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def reset_path(self) -> None:
        """Remove all path and visited overlays."""
        self.delete("path", "visited")
        self._path_objects.clear()
        self._visited_objects.clear()
        self._current_path.clear()

    def draw_maze(self, maze: Maze) -> None:
        """Initial draw – walls + passages."""
        self.maze = maze
        self.reset_path()
        self.delete("all")

        px = self.cell_px
        fw, fh = maze.w + 2, maze.h + 2  # frame size
        self.create_rectangle(0, 0, fw * px, fh * px, fill="black", outline="")

        for y in range(maze.h):
            for x in range(maze.w):
                colour = PALETTE.passage if maze.grid[y, x] else PALETTE.wall
                self._draw_rect(x, y, colour)

    def draw_cell(
        self, x: int, y: int, *, tag: str = "gen", colour: str | None = None
    ) -> None:
        """Low-level cell update (used by generators)."""
        if colour is None:
            colour = PALETTE.passage if self.maze and self.maze.grid[y, x] else PALETTE.wall
        self._draw_rect(x, y, colour, tag=tag)

    def add_visited_cell(
        self, x: int, y: int, *, colour: str | None = None
    ) -> None:
        """Small circle to mark explored cells."""
        if (x, y) in self._visited_objects:
            return
        colour = colour or PALETTE.visited
        obj_id = self._draw_oval(x, y, colour, tags="visited")
        self._visited_objects[(x, y)] = obj_id

    def draw_path(self, cells: Iterable[_Node]) -> None:
        """
        Incrementally update path overlay.
        Removes cells that left the path and adds new ones.
        """
        cells = list(cells)
        prev_set = set(self._current_path)
        curr_set = set(cells)

        # Visited markers for newly seen cells
        for xy in curr_set - prev_set:
            self.add_visited_cell(*xy)

        # Remove path circles no longer on route
        for xy in prev_set - curr_set:
            if xy in self._path_objects:
                self.delete(self._path_objects.pop(xy))

        # Add path circles for new positions
        for xy in curr_set - prev_set:
            obj_id = self._draw_oval(*xy, PALETTE.path, tags="path")
            self._path_objects[xy] = obj_id

        self._current_path = cells
        self.tag_raise("markers")  # keep start/goal on top

    def draw_markers(self, start: _Node, goal: _Node) -> None:
        """Draw start and goal dots."""
        self.delete("markers")
        pad = max(2, self.cell_px // 4)
        for (x, y), colour in ((start, PALETTE.start), (goal, PALETTE.goal)):
            obj_id = self._draw_oval(x, y, colour, pad=pad, tags="markers")
        self.tag_raise("markers")

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _draw_rect(
        self, x: int, y: int, colour: str, *, tag: str = ""
    ) -> int:
        """Rectangle for cell (x,y) including +1 border offset."""
        px = self.cell_px
        return self.create_rectangle(
            (x + 1) * px,
            (y + 1) * px,
            (x + 2) * px,
            (y + 2) * px,
            fill=colour,
            outline="",
            tags=tag,
        )

    def _draw_oval(
        self,
        x: int,
        y: int,
        colour: str,
        *,
        pad: int = 1,
        tags: str = "",
    ) -> int:
        """Circle inside cell (x,y) with optional padding."""
        px = self.cell_px
        return self.create_oval(
            (x + 1) * px + pad,
            (y + 1) * px + pad,
            (x + 2) * px - pad,
            (y + 2) * px - pad,
            fill=colour,
            outline="",
            tags=tags,
        )