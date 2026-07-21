"""Implementation of ``orion memory`` (stats / clear)."""

from __future__ import annotations

from pathlib import Path

from config import MEMORY_DATABASE_PATH
from memory.sqlite_memory import SQLiteMemory
from cli.output import ok_mark


def _format_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def _db_size(database_path: str) -> int:
    path = Path(database_path)
    return path.stat().st_size if path.exists() else 0


def _stats(memory: SQLiteMemory, database_path: str) -> int:
    entries = memory.count()
    rows = [
        ("Database", database_path),
        ("Entries", str(entries)),
        ("Size", _format_size(_db_size(database_path))),
    ]
    width = max(len(label) for label, _ in rows)
    for label, value in rows:
        print(f"{label.ljust(width)} : {value}")
    return 0


def _clear(memory: SQLiteMemory, *, confirm: bool) -> int:
    if not confirm:
        print("Refusing to clear memory without confirmation. Pass --yes.")
        return 1
    removed = memory.clear()
    print(
        f"{ok_mark()} Cleared memory "
        f"({removed} entr{'y' if removed == 1 else 'ies'})"
    )
    return 0


def run_memory(
    action: str,
    *,
    memory: SQLiteMemory | None = None,
    database_path: str | None = None,
    confirm: bool = False,
) -> int:
    """Dispatch an ``orion memory`` sub-action."""
    database_path = database_path or MEMORY_DATABASE_PATH
    owns_memory = memory is None
    if memory is None:
        memory = SQLiteMemory(database_path=database_path)

    try:
        if action == "stats":
            return _stats(memory, database_path)
        if action == "clear":
            return _clear(memory, confirm=confirm)
    finally:
        if owns_memory:
            memory.connection.close()

    print(f"Unknown memory action: {action}")
    return 2
