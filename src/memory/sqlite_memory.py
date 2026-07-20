import json
import sqlite3
from typing import Any

from memory.persistent_memory import PersistentMemory


class SQLiteMemory(PersistentMemory):

    def __init__(
        self,
        database_path: str = "orion_memory.db",
    ):
        self.connection = sqlite3.connect(
            database_path,
            check_same_thread=False,
        )

        self._create_table()

    def _create_table(self):

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

    # Step 4
    def set(
        self,
        key: str,
        value: Any,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO memory
            (key, value)

            VALUES (?, ?)
            """,
            (
                key,
                json.dumps(value),
            ),
        )

        self.connection.commit()

    # Step 5
    def get(
        self,
        key: str,
    ):

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

    # Step 6
    def delete(
        self,
        key: str,
    ):

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

    # Step 7
    def exists(
        self,
        key: str,
    ) -> bool:

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
