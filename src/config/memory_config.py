"""Persistent memory configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MemoryConfig:
    """Settings for Orion persistent memory storage."""

    database_path: str

    @classmethod
    def default(cls, project_root: Path) -> MemoryConfig:
        return cls(database_path=str(project_root / "orion_memory.db"))
