"""Top-level Orion configuration aggregate."""

from __future__ import annotations

from dataclasses import dataclass

from config.github_config import GitHubConfig
from config.memory_config import MemoryConfig
from config.runtime_config import RuntimeConfig
from errors import ConfigurationError


@dataclass(frozen=True)
class OrionConfig:
    """Typed configuration for the Orion platform."""

    github: GitHubConfig
    runtime: RuntimeConfig
    memory: MemoryConfig

    def validate(
        self,
        *,
        require_google_api_key: bool = False,
        require_github_token: bool = False,
    ) -> None:
        """
        Validate configuration values.

        Raises:
            ConfigurationError: when required settings are missing or invalid.
        """
        if not self.runtime.app_name or not str(self.runtime.app_name).strip():
            raise ConfigurationError(
                "APP_NAME must be a non-empty string",
                setting="APP_NAME",
            )

        if not self.github.api_base_url.startswith(("http://", "https://")):
            raise ConfigurationError(
                "GITHUB_API_BASE_URL must be an HTTP(S) URL",
                setting="GITHUB_API_BASE_URL",
            )

        if not self.memory.database_path or not str(
            self.memory.database_path
        ).strip():
            raise ConfigurationError(
                "Memory database path must be a non-empty string",
                setting="ORION_MEMORY_DB",
            )

        if require_google_api_key and not self.runtime.google_api_key:
            raise ConfigurationError(
                "GOOGLE_API_KEY is required to run Orion agents",
                setting="GOOGLE_API_KEY",
            )

        if require_github_token and not self.github.token:
            raise ConfigurationError(
                "GITHUB_TOKEN is required for authenticated GitHub operations",
                setting="GITHUB_TOKEN",
            )

    def __repr__(self) -> str:
        return (
            "OrionConfig("
            f"github={self.github!r}, "
            f"runtime={self.runtime!r}, "
            f"memory={self.memory!r})"
        )
