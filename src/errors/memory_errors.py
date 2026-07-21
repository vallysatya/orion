from .orion_error import OrionError


class OrionMemoryError(OrionError):
    """Base class for Orion memory failures."""


class MemoryOperationError(OrionMemoryError):
    """Raised when a memory operation fails."""

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        key: str | None = None,
    ) -> None:
        super().__init__(message)
        self.operation = operation
        self.key = key
