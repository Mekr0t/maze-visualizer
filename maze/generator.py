"""
Plug-in registry for maze-generation algorithms.

Any generator must implement::

    class MyGen:
        name: str = "unique-key"
        def __call__(self, w: int, h: int) -> Iterator[tuple[int, int, int]]:
            ...

The yielded tuple is (x, y, value) where value=0 → carve passage.
"""

from __future__ import annotations

__all__ = ["Generator", "register", "get_generator", "list_generators"]

from typing import Protocol, Iterator, Tuple, Dict, cast
from maze.maze import Maze  # noqa: F401 – used in type-checking only


class Generator(Protocol):
    """Protocol that every generator plugin must satisfy."""

    name: str

    def __call__(self, w: int, h: int) -> Iterator[Tuple[int, int, int]]: ...


# ------------------------------------------------------------------
# Tiny internal registry – keeps the module stateless and testable
# ------------------------------------------------------------------
_Registry: Dict[str, Generator] = {}


def register(cls: type[Generator]) -> type[Generator]:
    """
    Class decorator – adds an *instance* of the class to the registry.

    Raises:
        ValueError: if the chosen name is duplicated.
    """
    inst = cls()
    key = inst.name
    if key in _Registry:
        raise ValueError(f"Generator name {key!r} already registered")
    _Registry[key] = inst
    return cls


def get_generator(name: str) -> Generator:
    """
    Retrieve a generator instance by name.

    Raises:
        KeyError: if the name is unknown.
    """
    try:
        return _Registry[name]
    except KeyError as exc:
        raise KeyError(f"No generator named {name!r}") from exc


def list_generators() -> list[str]:
    """Return alphabetically sorted list of registered names."""
    return sorted(_Registry)