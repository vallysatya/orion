from .orion_error import OrionError


class ConfigurationError(OrionError):
    """Raised when Orion configuration is invalid."""

    def __init__(
        self,
        message: str,
        *,
        setting: str | None = None,
    ) -> None:
        super().__init__(message)
        self.setting = setting
