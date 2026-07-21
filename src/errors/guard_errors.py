from .orion_error import OrionError


class GuardError(OrionError):
    """Base class for guard-related failures."""


class GuardEvaluationError(GuardError):
    """Raised when a guard policy cannot be evaluated."""

    def __init__(
        self,
        message: str,
        *,
        tool_name: str | None = None,
        policy: str | None = None,
    ) -> None:
        super().__init__(message)
        self.tool_name = tool_name
        self.policy = policy
