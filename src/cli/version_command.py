"""Implementation of ``orion version``."""

from __future__ import annotations

from orion import __version__


def run_version() -> int:
    """Print the installed Orion version."""
    print(f"Orion {__version__}")
    return 0
