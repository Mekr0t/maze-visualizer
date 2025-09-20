"""
Depth-first search – fast but *not* optimal.
"""

from __future__ import annotations

__all__ = []

from typing import Iterator, List, Tuple

from maze.maze import Maze
from maze.solver import register
from utils.grid_helpers import neighbours

_Node = Tuple[int, int]


@register
class DFS:
    """Depth-First Search solver."""

    name: str = "DFS"

    def __call__(
        self, maze: Maze, start: _Node, goal: _Node
    ) -> Iterator[List[_Node]]:
        """
        Yield current DFS stack – last path is *a* route, not necessarily shortest.
        """
        stack: List[_Node] = [start]
        parent: dict[_Node, _Node | None] = {start: None}
        visited: set[_Node] = {start}

        while stack:
            current = stack.pop()
            path = self._reconstruct(parent, current)
            yield path
            if current == goal:
                return

            for nx, ny in neighbours(*current, maze.w, maze.h):
                if maze.grid[ny, nx] == 0 or (nx, ny) in visited:
                    continue
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                stack.append((nx, ny))

    # ------------------------------------------------------------------
    @staticmethod
    def _reconstruct(parent: dict[_Node, _Node | None], node: _Node) -> List[_Node]:
        path: List[_Node] = []
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path