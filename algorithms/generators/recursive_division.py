"""
Recursive-division maze generator.

Starts with an empty chamber and recursively subdivides it with walls,
leaving exactly one gap per wall.
"""

from __future__ import annotations

__all__ = []

import random
from typing import Iterator, List, Tuple

from maze.generator import register

# Orientation choices
_HORIZONTAL = True
_VERTICAL = False


@register
class RecursiveDivision:
    """Recursive division algorithm."""

    name: str = "Recursive Division"

    def __call__(self, width: int, height: int) -> Iterator[Tuple[int, int, int]]:
        """
        Generate a maze by recursive subdivision.

        Args:
            width:  total columns
            height: total rows

        Yields:
            ``(x, y, 1)`` → carve passage  
            ``(x, y, 0)`` → add wall
        """
        # 1. Start with open space
        for y in range(height):
            for x in range(width):
                yield (x, y, 1)

        # 2. Add outer border
        for x in range(width):
            yield (x, 0, 0)
            yield (x, height - 1, 0)
        for y in range(height):
            yield (0, y, 0)
            yield (width - 1, y, 0)

        # 3. Recursively subdivide
        yield from self._divide(0, 0, width, height)

        # 4. Guarantee entrance/exit
        yield (0, 1 if height > 2 else 0, 1)
        yield (width - 1, height - 2 if height > 2 else height - 1, 1)

    # ------------------------------------------------------------------
    # Recursive core
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Recursive core
    # ------------------------------------------------------------------
    def _divide(self, x: int, y: int, w: int, h: int) -> Iterator[Tuple[int, int, int]]:
        """Subdivide rectangle (x,y,w,h)."""
        if w < 3 or h < 3:
            return

        horizontal = self._pick_orientation(w, h)

        if horizontal:
            yield from self._split_horizontal(x, y, w, h)  # ← yield from
        else:
            yield from self._split_vertical(x, y, w, h)  # ← yield from

    def _split_horizontal(self, x: int, y: int, w: int, h: int) -> Iterator[Tuple[int, int, int]]:
        """Place horizontal wall with one gap."""
        wall_y = random.choice([yy for yy in range(y + 1, y + h - 1) if yy % 2 == 0])
        gap_x = random.choice([xx for xx in range(x, x + w) if xx % 2 == 1])

        for xx in range(x, x + w):
            if xx != gap_x:
                yield (xx, wall_y, 0)

        yield from self._divide(x, y, w, wall_y - y)
        yield from self._divide(x, wall_y + 1, w, y + h - (wall_y + 1))

    def _split_vertical(self, x: int, y: int, w: int, h: int) -> Iterator[Tuple[int, int, int]]:
        """Place vertical wall with one gap."""
        wall_x = random.choice([xx for xx in range(x + 1, x + w - 1) if xx % 2 == 0])
        gap_y = random.choice([yy for yy in range(y, y + h) if yy % 2 == 1])

        for yy in range(y, y + h):
            if yy != gap_y:
                yield (wall_x, yy, 0)

        yield from self._divide(x, y, wall_x - x, h)
        yield from self._divide(wall_x + 1, y, x + w - (wall_x + 1), h)

    def _pick_orientation(self, w: int, h: int) -> bool:
        """Return True if horizontal split preferred."""
        if h < w:
            return _VERTICAL
        if w < h:
            return _HORIZONTAL
        return random.choice([_HORIZONTAL, _VERTICAL])
