from .orion_error import OrionError


class ToolExecutionError(OrionError):
    """Raised when a tool execution fails."""

    def __init__(
        self,
        message: str,
        *,
        tool_name: str | None = None,
    ) -> None:
        super().__init__(message)
        self.tool_name = tool_name
