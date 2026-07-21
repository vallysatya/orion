"""SQLite-backed persistent memory for Orion."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from errors import MemoryOperationError
from memory.persistent_memory import PersistentMemory


class SQLiteMemory(PersistentMemory):
    """Persistent key/value store using SQLite."""

    def __init__(
        self,
        database_path: str = "orion_memory.db",
    ) -> None:
        try:
            self.connection = sqlite3.connect(
                database_path,
                check_same_thread=False,
            )
            self._create_table()
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to initialize SQLite memory",
                operation="initialize",
            ) from exc

    def _create_table(self) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            self.connection.commit()
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to create memory table",
                operation="create_table",
            ) from exc

    def set(self, key: str, value: Any) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO memory
                (key, value)
                VALUES (?, ?)
                """,
                (key, json.dumps(value)),
            )
            self.connection.commit()
        except (sqlite3.Error, TypeError, ValueError) as exc:
            raise MemoryOperationError(
                "Failed to write memory value",
                operation="set",
                key=key,
            ) from exc

    def get(self, key: str) -> Any:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT value
                FROM memory
                WHERE key = ?
                """,
                (key,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return json.loads(row[0])
        except (sqlite3.Error, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise MemoryOperationError(
                "Failed to read memory value",
                operation="get",
                key=key,
            ) from exc

    def delete(self, key: str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                DELETE
                FROM memory
                WHERE key = ?
                """,
                (key,),
            )
            self.connection.commit()
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to delete memory value",
                operation="delete",
                key=key,
            ) from exc

    def count(self) -> int:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            row = cursor.fetchone()
            return int(row[0]) if row else 0
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to count memory entries",
                operation="count",
            ) from exc

    def clear(self) -> int:
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM memory")
            self.connection.commit()
            return cursor.rowcount if cursor.rowcount != -1 else 0
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to clear memory",
                operation="clear",
            ) from exc

    def exists(self, key: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT 1
                FROM memory
                WHERE key = ?
                """,
                (key,),
            )
            return cursor.fetchone() is not None
        except sqlite3.Error as exc:
            raise MemoryOperationError(
                "Failed to check memory key",
                operation="exists",
                key=key,
            ) from exc
