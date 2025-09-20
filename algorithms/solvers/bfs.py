"""
Breadth-first search – guarantees shortest path in un-weighted grid.
"""

from __future__ import annotations

__all__ = []

from collections import deque
from typing import Iterator, List, Tuple

from maze.maze import Maze
from maze.solver import register
from utils.grid_helpers import neighbours

_Node = Tuple[int, int]


@register
class BFS:
    """Breadth-First Search solver."""

    name: str = "BFS"

    def __call__(
        self, maze: Maze, start: _Node, goal: _Node
    ) -> Iterator[List[_Node]]:
        """
        Yield progressively longer partial paths until the shortest is found.
        """
        queue: deque[_Node] = deque([start])
        parent: dict[_Node, _Node | None] = {start: None}
        visited: set[_Node] = {start}

        while queue:
            current = queue.popleft()
            path = self._reconstruct(parent, current)
            yield path
            if current == goal:
                return

            for nx, ny in neighbours(*current, maze.w, maze.h):
                if maze.grid[ny, nx] == 0 or (nx, ny) in visited:
                    continue
                visited.add((nx, ny))
                parent[(nx, ny)] = current
                queue.append((nx, ny))

    # ------------------------------------------------------------------
    @staticmethod
    def _reconstruct(parent: dict[_Node, _Node | None], node: _Node) -> List[_Node]:
        """Rebuild path from root to *node*."""
        path: List[_Node] = []
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path