"""
Maze-generation algorithms packaged as plug-ins.

Importing this sub-package automatically registers all bundled generators:

* DFS Backtracker (recursive depth-first)
* Kruskal (randomised MST)
* Prim (randomised Prim)
* Recursive Division (wall-adding)

Registered names can be listed via::

    from maze.generator import list_generators
    list_generators()
    ['DFS Backtracker', "Kruskal", "Prim's Algorithm", 'Recursive Division']
"""

from __future__ import annotations

# Side-effect: decorators execute and populate the central registry.
from . import dfs_backtracking, kruskals, prims, recursive_division

__all__ = []  # Nothing to export; registry is the single source of truth.