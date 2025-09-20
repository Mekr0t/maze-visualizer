"""
Core data container for a rectangular maze.

The coordinate system is (x, y) with origin at the top-left corner.
A cell value of 0 is interpreted as a passage, any non-zero value as a wall.
"""

from __future__ import annotations

__all__ = ["Maze"]

import numpy as np
from dataclasses import dataclass, field


@dataclass(slots=True)
class Maze:
    """
    Immutable width/height descriptor with a mutable numpy grid.

    Attributes:
        w: number of columns (x-axis)
        h: number of rows (y-axis)
        grid: uint8 numpy array shape (h, w).  0 == passage.
    """

    w: int
    h: int
    grid: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        if self.w <= 0 or self.h <= 0:
            raise ValueError("width and height must be positive")
        # ROW-MAJOR: grid[y, x] – matches screen convention
        self.grid = np.zeros((self.h, self.w), dtype=np.uint8)

    # ------------------------------------------------------------------
    # Convenience read-only properties (keeps callers from reaching in)
    # ------------------------------------------------------------------
    @property
    def shape(self) -> tuple[int, int]:
        """(w, h) tuple for quick unpacking."""
        return self.w, self.h