"""
Centralised colour palette for the maze visualiser.

All hex-strings are lowercase 6-digit RGB values without alpha.
Change this file to re-theme the entire project.
"""

from __future__ import annotations

from typing import Final, NamedTuple

__all__ = ["Palette", "PALETTE"]


class Palette(NamedTuple):
    """Immutable colour theme used during rendering."""

    wall: str = "#222831"      # dark slate
    passage: str = "#eeeeee"   # almost white
    path: str = "#00adb5"      # cyan accent
    frontier: str = "#ffd369"  # warm yellow
    visited: str = "#393e46"   # mid slate
    start: str = "#28a745"     # bootstrap green
    goal: str = "#e53935"      # material red


# Single instance exported to the rest of the project.
PALETTE: Final[Palette] = Palette()