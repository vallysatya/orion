"""
Shared application configuration package.

Preserves historical module-level exports used across Orion:
  from config import APP_NAME, GITHUB_TOKEN, validate_configuration, ...
"""

from __future__ import annotations

from config.config import OrionConfig
from config.github_config import GitHubConfig
from config.loader import PROJECT_ROOT, SRC_DIR, ConfigLoader
from config.memory_config import MemoryConfig
from config.runtime_config import RuntimeConfig
from errors import ConfigurationError

_loader = ConfigLoader()
_settings: OrionConfig = _loader.load()

# ------------------------------------------------------------------
# Backward-compatible module-level exports
# ------------------------------------------------------------------

GOOGLE_API_KEY = _settings.runtime.google_api_key
GITHUB_TOKEN = _settings.github.token
GITHUB_API_BASE_URL = _settings.github.api_base_url
APP_NAME = _settings.runtime.app_name
DEFAULT_USER_ID = _settings.runtime.default_user_id
DEFAULT_SESSION_ID = _settings.runtime.default_session_id
MEMORY_DATABASE_PATH = _settings.memory.database_path
ORION_DEBUG = _settings.runtime.debug


def get_settings() -> OrionConfig:
    """Return the loaded OrionConfig instance."""
    return _settings


def reload_settings(
    *,
    environ: dict[str, str] | None = None,
    load_dotenv_files: bool = False,
) -> OrionConfig:
    """
    Reload settings (primarily for tests).

    Updates module-level compatibility exports in-place.
    """
    global _settings
    global GOOGLE_API_KEY, GITHUB_TOKEN, GITHUB_API_BASE_URL
    global APP_NAME, DEFAULT_USER_ID, DEFAULT_SESSION_ID
    global MEMORY_DATABASE_PATH, ORION_DEBUG

    loader = ConfigLoader(
        environ=environ,
        load_dotenv_files=load_dotenv_files,
    )
    _settings = loader.load()

    GOOGLE_API_KEY = _settings.runtime.google_api_key
    GITHUB_TOKEN = _settings.github.token
    GITHUB_API_BASE_URL = _settings.github.api_base_url
    APP_NAME = _settings.runtime.app_name
    DEFAULT_USER_ID = _settings.runtime.default_user_id
    DEFAULT_SESSION_ID = _settings.runtime.default_session_id
    MEMORY_DATABASE_PATH = _settings.memory.database_path
    ORION_DEBUG = _settings.runtime.debug
    return _settings


def validate_configuration(
    *,
    require_google_api_key: bool = False,
    require_github_token: bool = False,
) -> None:
    """
    Validate Orion configuration.

    Reads current module-level exports so monkeypatch-based tests continue
    to work, without ever putting secret values into error messages.
    """
    cfg = OrionConfig(
        github=GitHubConfig(
            api_base_url=GITHUB_API_BASE_URL,
            token=GITHUB_TOKEN,
        ),
        runtime=RuntimeConfig(
            app_name=APP_NAME,
            default_user_id=DEFAULT_USER_ID,
            default_session_id=DEFAULT_SESSION_ID,
            google_api_key=GOOGLE_API_KEY,
            debug=ORION_DEBUG,
        ),
        memory=MemoryConfig(database_path=MEMORY_DATABASE_PATH),
    )
    cfg.validate(
        require_google_api_key=require_google_api_key,
        require_github_token=require_github_token,
    )


__all__ = [
    "APP_NAME",
    "ConfigurationError",
    "ConfigLoader",
    "DEFAULT_SESSION_ID",
    "DEFAULT_USER_ID",
    "GITHUB_API_BASE_URL",
    "GITHUB_TOKEN",
    "GOOGLE_API_KEY",
    "GitHubConfig",
    "MEMORY_DATABASE_PATH",
    "MemoryConfig",
    "ORION_DEBUG",
    "OrionConfig",
    "PROJECT_ROOT",
    "RuntimeConfig",
    "SRC_DIR",
    "get_settings",
    "reload_settings",
    "validate_configuration",
]
