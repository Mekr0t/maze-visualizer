"""
Dijkstra’s algorithm – uniform-cost search (no heuristic).
"""

from __future__ import annotations

__all__ = []

import heapq
from typing import Iterator, List, Tuple

from maze.maze import Maze
from maze.solver import register
from utils.grid_helpers import neighbours

_Cost = int
_Node = Tuple[int, int]


@register
class Dijkstra:
    """Uniform-cost search solver."""

    name: str = "Dijkstra"

    def __call__(
        self, maze: Maze, start: _Node, goal: _Node
    ) -> Iterator[List[_Node]]:
        """
        Yield best-known paths until the shortest is found.
        """
        dist: dict[_Node, _Cost] = {start: 0}
        parent: dict[_Node, _Node | None] = {start: None}
        pq: list[tuple[_Cost, _Node]] = [(0, start)]
        visited: set[_Node] = set()

        while pq:
            cost, current = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)

            path = self._reconstruct(parent, current)
            yield path
            if current == goal:
                return

            x, y = current
            for nx, ny in neighbours(x, y, maze.w, maze.h):
                if maze.grid[ny, nx] == 0:
                    continue  # wall
                new_cost = cost + 1
                if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                    dist[(nx, ny)] = new_cost
                    parent[(nx, ny)] = current
                    heapq.heappush(pq, (new_cost, (nx, ny)))

    # ------------------------------------------------------------------
    @staticmethod
    def _reconstruct(parent: dict[_Node, _Node | None], node: _Node) -> List[_Node]:
        path: List[_Node] = []
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path