"""
Randomised Prim minimum-spanning-tree maze generator.

Starts from an arbitrary cell and grows the maze by adding random
frontier walls.
"""

from __future__ import annotations

__all__ = []

import random
from typing import Iterator, List, Tuple

from maze.generator import register

# 2-step moves to keep 1-cell thick walls
_MOVES = [(2, 0), (-2, 0), (0, 2), (0, -2)]


@register
class Prim:
    """Randomised Prim algorithm."""

    name: str = "Prim's Algorithm"

    def __call__(self, width: int, height: int) -> Iterator[Tuple[int, int, int]]:
        """
        Generate a maze via Prim's algorithm.

        Args:
            width:  columns (forced to odd)
            height: rows    (forced to odd)

        Yields:
            ``(x, y, 1)`` for every carved passage.
        """
        w, h = self._force_odd(width, height)
        visited = [[False] * w for _ in range(h)]
        frontiers: List[Tuple[int, int, int, int]] = []

        def add_frontiers(x: int, y: int) -> None:
            """Append frontier walls surrounding (x,y)."""
            for dx, dy in _MOVES:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                    frontiers.append((x + dx // 2, y + dy // 2, nx, ny))

        # Start carving
        visited[0][0] = True
        yield (0, 0, 1)
        add_frontiers(0, 0)

        while frontiers:
            wx, wy, nx, ny = frontiers.pop(random.randrange(len(frontiers)))
            if not visited[ny][nx]:
                visited[ny][nx] = True
                yield (wx, wy, 1)
                yield (nx, ny, 1)
                add_frontiers(nx, ny)

    # ------------------------------------------------------------------
    @staticmethod
    def _force_odd(w: int, h: int) -> Tuple[int, int]:
        """Return odd dimensions ≥ original."""
        return (w - 1 if w % 2 == 0 else w), (h - 1 if h % 2 == 0 else h)