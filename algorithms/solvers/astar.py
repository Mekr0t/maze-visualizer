"""
A* shortest-path algorithm with Manhattan heuristic.
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
class AStar:
    """A* with Manhattan distance heuristic."""

    name: str = "A*"

    def __call__(
        self, maze: Maze, start: _Node, goal: _Node
    ) -> Iterator[List[_Node]]:
        """
        Yield increasingly better paths from *start* to *goal*.

        The last yielded path is optimal.
        """
        cx, cy = start

        def heuristic(x: int, y: int) -> _Cost:
            return abs(x - goal[0]) + abs(y - goal[1])

        # (f, g, node, path)
        pq: List[Tuple[_Cost, _Cost, _Node, List[_Node]]] = [
            (heuristic(*start), 0, start, [start])
        ]
        visited: set[_Node] = set()

        while pq:
            _, cost, (x, y), path = heapq.heappop(pq)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            yield path

            if (x, y) == goal:
                return

            for nx, ny in neighbours(x, y, maze.w, maze.h):
                if maze.grid[ny, nx] == 0 or (nx, ny) in visited:
                    continue
                new_cost = cost + 1
                heapq.heappush(
                    pq,
                    (new_cost + heuristic(nx, ny), new_cost, (nx, ny), path + [(nx, ny)]),
                )