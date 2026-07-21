"""Implementation of ``orion doctor``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config import OrionConfig, get_settings
from errors import ConfigurationError, OrionError
from cli.output import fail_mark, ok_mark


@dataclass(frozen=True)
class DoctorCheck:
    """One configuration or dependency health check."""

    label: str
    healthy: bool
    detail: str | None = None


def _check_github_token(settings: OrionConfig) -> DoctorCheck:
    configured = bool(settings.github.token)
    return DoctorCheck(
        "GitHub token configured",
        configured,
        None if configured else "set GITHUB_TOKEN",
    )


def _check_repository(app_container: Any) -> DoctorCheck:
    try:
        repository = (
            app_container.persistent_memory.get("default_repository")
            or app_container.persistent_memory.get("current_repository")
        )
    except OrionError as exc:
        return DoctorCheck(
            "Repository configured",
            False,
            type(exc).__name__,
        )

    configured = bool(repository)
    return DoctorCheck(
        "Repository configured",
        configured,
        None if configured else "select or remember a repository",
    )


def _check_memory(app_container: Any) -> DoctorCheck:
    try:
        # Read-only probe through the shared persistent-memory dependency.
        app_container.persistent_memory.exists("__orion_doctor_probe__")
    except OrionError as exc:
        return DoctorCheck(
            "Memory database available",
            False,
            type(exc).__name__,
        )
    return DoctorCheck("Memory database available", True)


def _check_model_configuration(settings: OrionConfig) -> DoctorCheck:
    try:
        settings.validate(require_google_api_key=True)
    except ConfigurationError as exc:
        return DoctorCheck(
            "Model/API configuration valid",
            False,
            exc.setting,
        )
    return DoctorCheck("Model/API configuration valid", True)


def collect_checks(
    *,
    settings: OrionConfig | None = None,
    app_container: Any | None = None,
) -> tuple[DoctorCheck, ...]:
    """Run all diagnostics using shared configuration and dependencies."""
    if settings is None:
        settings = get_settings()
    if app_container is None:
        # Lazy import prevents unrelated commands from initializing storage.
        from container import container as shared_container

        app_container = shared_container

    return (
        _check_github_token(settings),
        _check_repository(app_container),
        _check_memory(app_container),
        _check_model_configuration(settings),
    )


def run_doctor(
    *,
    settings: OrionConfig | None = None,
    app_container: Any | None = None,
) -> int:
    """Print Orion health checks; return non-zero if any fail."""
    checks = collect_checks(
        settings=settings,
        app_container=app_container,
    )
    for check in checks:
        symbol = ok_mark() if check.healthy else fail_mark()
        detail = f" ({check.detail})" if check.detail else ""
        print(f"{symbol} {check.label}{detail}")

    return 0 if all(check.healthy for check in checks) else 1
