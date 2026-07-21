from .orion_error import OrionError


class OrionRuntimeError(OrionError):
    """Raised when the Orion runtime fails."""

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        session_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.operation = operation
        self.session_id = session_id
