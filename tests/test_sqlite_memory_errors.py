"""SQLiteMemory error-wrapping tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from errors import MemoryOperationError, OrionError, OrionMemoryError
from memory.sqlite_memory import SQLiteMemory


def test_sqlite_memory_round_trip(tmp_path):
    memory = SQLiteMemory(database_path=str(tmp_path / "memory.db"))

    memory.set("user_name", "Vally")
    assert memory.get("user_name") == "Vally"
    assert memory.exists("user_name") is True

    memory.delete("user_name")
    assert memory.exists("user_name") is False
    assert memory.get("user_name") is None


def test_sqlite_memory_wraps_set_failures(tmp_path):
    memory = SQLiteMemory(database_path=str(tmp_path / "memory.db"))
    memory.connection = MagicMock()
    memory.connection.cursor.side_effect = Exception("boom")

    # sqlite3.Error subclass path — use a real sqlite3.Error
    import sqlite3

    memory.connection.cursor.side_effect = sqlite3.OperationalError("disk I/O error")

    with pytest.raises(MemoryOperationError) as exc_info:
        memory.set("user_name", "Vally")

    error = exc_info.value
    assert isinstance(error, OrionMemoryError)
    assert isinstance(error, OrionError)
    assert error.operation == "set"
    assert error.key == "user_name"
    assert isinstance(error.__cause__, sqlite3.OperationalError)


def test_sqlite_memory_wraps_get_failures(tmp_path):
    import sqlite3

    memory = SQLiteMemory(database_path=str(tmp_path / "memory.db"))
    memory.connection = MagicMock()
    memory.connection.cursor.side_effect = sqlite3.DatabaseError("corrupt")

    with pytest.raises(MemoryOperationError) as exc_info:
        memory.get("user_name")

    assert exc_info.value.operation == "get"
    assert isinstance(exc_info.value.__cause__, sqlite3.DatabaseError)


def test_sqlite_memory_wraps_non_serializable_set(tmp_path):
    memory = SQLiteMemory(database_path=str(tmp_path / "memory.db"))

    with pytest.raises(MemoryOperationError) as exc_info:
        memory.set("bad", object())

    assert exc_info.value.operation == "set"
    assert isinstance(exc_info.value.__cause__, TypeError)
