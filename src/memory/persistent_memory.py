from abc import ABC, abstractmethod
from typing import Any


class PersistentMemory(ABC):
    """
    Abstract interface for Orion persistent memory.

    Implementations may use SQLite, PostgreSQL,
    Redis, Firestore, etc.
    """

    @abstractmethod
    def get(self, key: str) -> Any:
        """
        Retrieve a value from persistent storage.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Persist a value.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Remove a value.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check whether a key exists.
        """
        pass
