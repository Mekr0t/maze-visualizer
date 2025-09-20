"""
Frame-rate throttling utilities.

This module is independent of any graphics library and can be reused
in any project that needs to cap the speed of a generator loop.
"""

from __future__ import annotations

import time
from typing import Any, Iterator

__all__ = ["throttle"]


def throttle(iterator: Iterator[Any], *, fps: int = 60) -> Iterator[Any]:
    """
    Yield items from *iterator* while respecting a maximum frame-rate.

    Args:
        iterator: Any iterable / generator you want to slow down.
        fps: Desired frames (iterations) per second. Must be > 0.

    Yields:
        The exact same objects produced by *iterator*, but spaced out in time.

    Raises:
        ValueError: if *fps* is not positive.

    Example:
         for row in throttle(big_query_result, fps=30):
            render(row)
    """
    if fps <= 0:
        raise ValueError("fps must be positive")

    frame_time = 1.0 / fps
    last_tick = time.perf_counter()

    for item in iterator:
        now = time.perf_counter()
        sleep_for = frame_time - (now - last_tick)
        if sleep_for > 0:
            time.sleep(sleep_for)
        last_tick = time.perf_counter()
        yield item