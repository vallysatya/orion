from .orion_error import OrionError


class IntegrationError(OrionError):
    """Base integration error."""


class GitHubIntegrationError(IntegrationError):
    """Raised when GitHub communication fails."""

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        method: str | None = None,
        endpoint: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.operation = operation
        self.method = method
        self.endpoint = endpoint
        self.status_code = status_code
