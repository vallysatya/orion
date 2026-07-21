"""Environment loading and parsing for Orion configuration."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv

from config.github_config import GitHubConfig
from config.memory_config import MemoryConfig
from config.runtime_config import RuntimeConfig
from errors import ConfigurationError

if TYPE_CHECKING:
    from config.config import OrionConfig

SRC_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SRC_DIR.parent


class ConfigLoader:
    """Loads Orion settings from dotenv files and process environment."""

    def __init__(
        self,
        *,
        project_root: Path | None = None,
        src_dir: Path | None = None,
        environ: dict[str, str] | None = None,
        load_dotenv_files: bool = True,
    ) -> None:
        self._project_root = project_root or PROJECT_ROOT
        self._src_dir = src_dir or SRC_DIR
        self._environ = environ if environ is not None else os.environ
        self._load_dotenv_files = load_dotenv_files

    def load_dotenv_files(self) -> None:
        """Load known .env locations (project + agent paths)."""
        load_dotenv(self._project_root / ".env")
        load_dotenv(self._src_dir / "agents" / "github_agent" / ".env")
        # Legacy / alternate path
        load_dotenv(self._src_dir / "github_agent" / ".env", override=True)

    def get(self, name: str, default: str | None = None) -> str | None:
        value = self._environ.get(name, default)
        if value is None:
            return None
        value = value.strip()
        return value if value else None

    def parse_bool(self, name: str, default: bool = False) -> bool:
        """Parse a boolean environment variable."""
        raw = self.get(name)
        if raw is None:
            return default

        normalized = raw.lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False

        raise ConfigurationError(
            f"Invalid boolean value for {name}",
            setting=name,
        )

    def load_github_config(self) -> GitHubConfig:
        # Preserve historical default: base URL is fixed unless explicitly set.
        return GitHubConfig(
            api_base_url=self.get(
                "GITHUB_API_BASE_URL",
                "https://api.github.com",
            )
            or "https://api.github.com",
            token=self.get("GITHUB_TOKEN"),
        )

    def load_runtime_config(self) -> RuntimeConfig:
        # Preserve historical defaults for app/session identifiers.
        return RuntimeConfig(
            app_name=self.get("ORION_APP_NAME", "orion") or "orion",
            default_user_id=self.get("ORION_DEFAULT_USER_ID", "default-user")
            or "default-user",
            default_session_id=self.get(
                "ORION_DEFAULT_SESSION_ID",
                "default_session",
            )
            or "default_session",
            google_api_key=self.get("GOOGLE_API_KEY"),
            debug=self.parse_bool("ORION_DEBUG", default=False),
        )

    def load_memory_config(self) -> MemoryConfig:
        custom_path = self.get("ORION_MEMORY_DB")
        if custom_path:
            return MemoryConfig(database_path=custom_path)
        return MemoryConfig.default(self._project_root)

    def load(self) -> OrionConfig:
        """Build a full OrionConfig from the environment."""
        from config.config import OrionConfig

        if self._load_dotenv_files:
            self.load_dotenv_files()

        return OrionConfig(
            github=self.load_github_config(),
            runtime=self.load_runtime_config(),
            memory=self.load_memory_config(),
        )
