"""
Depth-first search back-tracking maze generator.

Yields (x, y, value) tuples where value == 1  → carve passage.
Works on odd-width/height grids to guarantee perfect 1-cell-thick walls.
"""

from __future__ import annotations

__all__ = []

import random
from typing import Iterator, List, Tuple

from maze.generator import register

# 2-step moves keep 1-cell wall between carved cells.
_TWO_STEP_MOVES: List[Tuple[int, int]] = [(2, 0), (-2, 0), (0, 2), (0, -2)]


@register
class DFSBacktracker:
    """Classic recursive DFS maze generator (iterative implementation)."""

    name: str = "DFS Backtracker"

    def __call__(self, width: int, height: int) -> Iterator[Tuple[int, int, int]]:
        """
        Generate a maze by iterative depth-first search.

        Args:
            width:  desired number of columns (will be forced to odd)
            height: desired number of rows (will be forced to odd)

        Yields:
            Tuples ``(x, y, 1)`` for every carved passage.
        """
        w, h = self._ensure_odd(width, height)
        visited = [[False] * w for _ in range(h)]
        stack: List[Tuple[int, int]] = [(0, 0)]
        visited[0][0] = True
        yield (0, 0, 1)

        while stack:
            x, y = stack[-1]
            candidates = self._unvisited_two_step_neighbours(x, y, w, h, visited)

            if not candidates:
                stack.pop()
                continue

            nx, ny = random.choice(candidates)
            visited[ny][nx] = True

            # Carve the wall between (x,y) and (nx,ny)
            wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
            yield (wall_x, wall_y, 1)
            yield (nx, ny, 1)

            stack.append((nx, ny))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _ensure_odd(w: int, h: int) -> Tuple[int, int]:
        """Return odd dimensions ≥ original."""
        return (w - 1 if w % 2 == 0 else w), (h - 1 if h % 2 == 0 else h)

    @staticmethod
    def _unvisited_two_step_neighbours(
        x: int, y: int, w: int, h: int, visited: List[List[bool]]
    ) -> List[Tuple[int, int]]:
        """Return 2-step neighbours that are still unvisited."""
        nbrs: List[Tuple[int, int]] = []
        for dx, dy in _TWO_STEP_MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                nbrs.append((nx, ny))
        return nbrs