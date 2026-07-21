"""Runtime / application configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    """Settings for Orion runtime and agent execution."""

    app_name: str = "orion"
    default_user_id: str = "default-user"
    default_session_id: str = "default_session"
    google_api_key: str | None = None
    debug: bool = False

    def __repr__(self) -> str:
        key_display = "***" if self.google_api_key else None
        return (
            "RuntimeConfig("
            f"app_name={self.app_name!r}, "
            f"default_user_id={self.default_user_id!r}, "
            f"default_session_id={self.default_session_id!r}, "
            f"google_api_key={key_display!r}, "
            f"debug={self.debug!r})"
        )
