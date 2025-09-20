"""
Randomised Kruskal minimum-spanning-tree maze generator.

Treats each odd coordinate cell as a vertex and randomly adds
walls (edges) until a spanning tree exists.
"""

from __future__ import annotations

__all__ = []

import random
from typing import Iterator, Tuple, Dict, List, Set

from maze.generator import register

# Union-Find helpers
_Node = Tuple[int, int]


@register
class Kruskal:
    """Randomised Kruskal algorithm."""

    name: str = "Kruskal"

    def __call__(self, width: int, height: int) -> Iterator[Tuple[int, int, int]]:
        """
        Generate a maze via Kruskal's algorithm.

        Args:
            width:  columns (odd values work best)
            height: rows    (odd values work best)

        Yields:
            ``(x, y, 1)`` for every carved passage.
        """
        w, h = width, height
        parent: Dict[_Node, _Node] = {}
        uf = _UnionFind(parent)

        # 1. Carve all odd-coordinate cells and initialise UF
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                parent[(x, y)] = (x, y)
                yield (x, y, 1)

        # 2. Build edge list (walls between adjacent odd cells)
        edges: List[Tuple[_Node, _Node, _Node]] = []  # (a, b, wall)
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                if x + 2 < w:
                    edges.append(((x, y), (x + 2, y), (x + 1, y)))
                if y + 2 < h:
                    edges.append(((x, y), (x, y + 2), (x, y + 1)))

        random.shuffle(edges)

        # 3. Process edges
        for a, b, wall in edges:
            if uf.union(a, b):
                yield (wall[0], wall[1], 1)
                yield (b[0], b[1], 1)


class _UnionFind:
    """Internal union-find for Kruskal."""
    __slots__ = ("parent",)

    def __init__(self, parent: Dict[_Node, _Node]) -> None:
        self.parent = parent

    def find(self, item: _Node) -> _Node:
        """Path-halving find."""
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, a: _Node, b: _Node) -> bool:
        """Return True if two sets were merged."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True