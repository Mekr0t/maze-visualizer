"""
Path-finding algorithms packaged as plug-ins.

Importing this sub-package automatically registers all bundled solvers:

* A* (Manhattan heuristic)
* BFS (shortest path in un-weighted grid)
* DFS (depth-first, not optimal)
* Dijkstra (uniform-cost, no heuristic)

Registered names can be listed via::

    >>> from maze.solver import list_solvers
    >>> list_solvers()
    ['A*', 'BFS', 'DFS', "Dijkstra"]
"""

from __future__ import annotations

# Side-effect: decorators populate the central registry.
from . import astar, bfs, dfs, dijkstra

__all__ = []