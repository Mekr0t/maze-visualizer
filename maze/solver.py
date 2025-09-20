"""
Plug-in registry for path-finding algorithms.

A solver must implement::

    class MySolver:
        name: str = "unique-key"
        def __call__(
            self, maze: Maze, start: tuple[int, int], goal: tuple[int, int]
        ) -> Iterator[list[tuple[int, int]]]:
            ...

The outer iterator yields *intermediate* paths (for animation), the last
item is the final optimal route.  If no route exists the iterator is empty.
"""

from __future__ import annotations

__all__ = ["Solver", "register", "get_solver", "list_solvers"]

from typing import Protocol, Iterator, List, Tuple, Dict, cast
from maze.maze import Maze


class Solver(Protocol):
    """Protocol that every solver plugin must satisfy."""

    name: str

    def __call__(
        self, maze: Maze, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> Iterator[List[Tuple[int, int]]]: ...


# ------------------------------------------------------------------
# Internal registry – symmetrical to generator.py
# ------------------------------------------------------------------
_Registry: Dict[str, Solver] = {}


def register(cls: type[Solver]) -> type[Solver]:
    """
    Class decorator – adds an *instance* of the class to the registry.

    Raises:
        ValueError: if the chosen name is duplicated.
    """
    inst = cls()
    key = inst.name
    if key in _Registry:
        raise ValueError(f"Solver name {key!r} already registered")
    _Registry[key] = inst
    return cls


def get_solver(name: str) -> Solver:
    """
    Retrieve a solver instance by name.

    Raises:
        KeyError: if the name is unknown.
    """
    try:
        return _Registry[name]
    except KeyError as exc:
        raise KeyError(f"No solver named {name!r}") from exc


def list_solvers() -> list[str]:
    """Return alphabetically sorted list of registered names."""
    return sorted(_Registry)