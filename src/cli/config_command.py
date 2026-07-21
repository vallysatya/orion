"""Implementation of ``orion config`` (show / validate / init)."""

from __future__ import annotations

from pathlib import Path

from config import OrionConfig, get_settings
from errors import ConfigurationError
from cli.output import fail_mark, ok_mark

_ENV_TEMPLATE = """\
# Orion configuration
# Copy this file to .env and fill in the values below.

# --- GitHub integration ---
GITHUB_TOKEN=
GITHUB_API_BASE_URL=https://api.github.com

# --- Runtime ---
GOOGLE_API_KEY=
ORION_APP_NAME=orion
ORION_DEFAULT_USER_ID=default-user
ORION_DEFAULT_SESSION_ID=default_session
ORION_DEBUG=false

# --- Memory ---
# Absolute or relative path to the SQLite database file.
ORION_MEMORY_DB=
"""


def _mask(value: str | None) -> str:
    """Return a redacted marker for secrets, never the raw value."""
    return "********" if value else "(not set)"


def _show(settings: OrionConfig) -> int:
    rows = [
        ("App name", settings.runtime.app_name),
        ("GitHub API", settings.github.api_base_url),
        ("GitHub token", _mask(settings.github.token)),
        ("Google API key", _mask(settings.runtime.google_api_key)),
        ("Default user", settings.runtime.default_user_id),
        ("Default session", settings.runtime.default_session_id),
        ("Memory database", settings.memory.database_path),
        ("Debug", str(settings.runtime.debug)),
    ]
    width = max(len(label) for label, _ in rows)
    for label, value in rows:
        print(f"{label.ljust(width)} : {value}")
    return 0


def _validate(settings: OrionConfig) -> int:
    try:
        settings.validate()
    except ConfigurationError as exc:
        print(f"{fail_mark()} Invalid configuration ({exc.setting}): {exc}")
        return 1
    print(f"{ok_mark()} Configuration is valid")
    return 0


def _init(target: Path, *, force: bool = False) -> int:
    if target.exists() and not force:
        print(
            f"{fail_mark()} {target} already exists "
            "(use --force to overwrite)"
        )
        return 1
    target.write_text(_ENV_TEMPLATE, encoding="utf-8")
    print(f"{ok_mark()} Wrote configuration template to {target}")
    return 0


def run_config(
    action: str,
    *,
    settings: OrionConfig | None = None,
    target: Path | None = None,
    force: bool = False,
) -> int:
    """Dispatch an ``orion config`` sub-action."""
    if action == "init":
        return _init(target or Path(".env.example"), force=force)

    if settings is None:
        settings = get_settings()

    if action == "show":
        return _show(settings)
    if action == "validate":
        return _validate(settings)

    print(f"Unknown config action: {action}")
    return 2
