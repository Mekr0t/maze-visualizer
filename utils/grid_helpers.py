"""
Pure helper functions for 2-D rectangular grids.

Coordinates are always (x, y) with origin at top-left.
All functions are boundary-safe.
"""

from __future__ import annotations

from typing import Final, List, Tuple

__all__ = ["neighbours"]

# 4-connected von Neumann neighbourhood.
_FOUR_DIRS: Final[List[Tuple[int, int]]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def neighbours(x: int, y: int, width: int, height: int) -> List[Tuple[int, int]]:
    """
    Return 4-connected neighbours of cell (x, y) that lie inside the grid.

    Args:
        x: Column index (0-based).
        y: Row index (0-based).
        width: Total number of columns.
        height: Total number of rows.

    Returns:
        List of (nx, ny) tuples, possibly empty.
    """
    result: List[Tuple[int, int]] = []
    for dx, dy in _FOUR_DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            result.append((nx, ny))
    return result