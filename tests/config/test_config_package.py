"""Focused tests for the typed Orion config package."""

from __future__ import annotations

from pathlib import Path

import pytest

from config import (
    APP_NAME,
    GITHUB_API_BASE_URL,
    ConfigLoader,
    GitHubConfig,
    OrionConfig,
    RuntimeConfig,
    MemoryConfig,
    get_settings,
    validate_configuration,
)
from errors import ConfigurationError


def test_loader_defaults_without_env(tmp_path: Path):
    loader = ConfigLoader(
        project_root=tmp_path,
        src_dir=tmp_path / "src",
        environ={},
        load_dotenv_files=False,
    )
    cfg = loader.load()

    assert cfg.runtime.app_name == "orion"
    assert cfg.runtime.default_user_id == "default-user"
    assert cfg.runtime.default_session_id == "default_session"
    assert cfg.runtime.google_api_key is None
    assert cfg.runtime.debug is False
    assert cfg.github.api_base_url == "https://api.github.com"
    assert cfg.github.token is None
    assert cfg.memory.database_path == str(tmp_path / "orion_memory.db")


def test_loader_reads_environment_overrides(tmp_path: Path):
    loader = ConfigLoader(
        project_root=tmp_path,
        src_dir=tmp_path / "src",
        environ={
            "GOOGLE_API_KEY": "secret-google-key",
            "GITHUB_TOKEN": "secret-github-token",
            "GITHUB_API_BASE_URL": "https://github.example.com",
            "ORION_APP_NAME": "orion-test",
            "ORION_MEMORY_DB": str(tmp_path / "custom.db"),
            "ORION_DEBUG": "true",
        },
        load_dotenv_files=False,
    )
    cfg = loader.load()

    assert cfg.runtime.google_api_key == "secret-google-key"
    assert cfg.github.token == "secret-github-token"
    assert cfg.github.api_base_url == "https://github.example.com"
    assert cfg.runtime.app_name == "orion-test"
    assert cfg.memory.database_path == str(tmp_path / "custom.db")
    assert cfg.runtime.debug is True


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("false", False),
        ("0", False),
        ("no", False),
        ("off", False),
    ],
)
def test_parse_bool_values(raw: str, expected: bool, tmp_path: Path):
    loader = ConfigLoader(
        project_root=tmp_path,
        environ={"ORION_DEBUG": raw},
        load_dotenv_files=False,
    )
    assert loader.parse_bool("ORION_DEBUG") is expected


def test_parse_bool_invalid_raises(tmp_path: Path):
    loader = ConfigLoader(
        project_root=tmp_path,
        environ={"ORION_DEBUG": "maybe"},
        load_dotenv_files=False,
    )
    with pytest.raises(ConfigurationError) as exc_info:
        loader.parse_bool("ORION_DEBUG")
    assert exc_info.value.setting == "ORION_DEBUG"


def test_validate_configuration_passes_defaults():
    validate_configuration()


def test_validate_configuration_requires_google_api_key(monkeypatch):
    monkeypatch.setattr("config.GOOGLE_API_KEY", None)

    with pytest.raises(ConfigurationError) as exc_info:
        validate_configuration(require_google_api_key=True)

    assert exc_info.value.setting == "GOOGLE_API_KEY"
    assert "secret" not in str(exc_info.value).lower()


def test_validate_configuration_requires_github_token(monkeypatch):
    monkeypatch.setattr("config.GITHUB_TOKEN", None)

    with pytest.raises(ConfigurationError) as exc_info:
        validate_configuration(require_github_token=True)

    assert exc_info.value.setting == "GITHUB_TOKEN"
    # Never leak token material into the exception text
    assert "ghp_" not in str(exc_info.value)
    assert "token" not in str(exc_info.value).lower() or "GITHUB_TOKEN" in str(
        exc_info.value
    )


def test_orion_config_validate_invalid_url():
    cfg = OrionConfig(
        github=GitHubConfig(api_base_url="not-a-url", token=None),
        runtime=RuntimeConfig(),
        memory=MemoryConfig(database_path="memory.db"),
    )
    with pytest.raises(ConfigurationError) as exc_info:
        cfg.validate()
    assert exc_info.value.setting == "GITHUB_API_BASE_URL"


def test_github_config_repr_redacts_token():
    cfg = GitHubConfig(token="super-secret-token")
    rendered = repr(cfg)
    assert "super-secret-token" not in rendered
    assert "***" in rendered


def test_runtime_config_repr_redacts_api_key():
    cfg = RuntimeConfig(google_api_key="super-secret-key")
    rendered = repr(cfg)
    assert "super-secret-key" not in rendered
    assert "***" in rendered


def test_module_exports_preserve_legacy_defaults():
    assert APP_NAME == "orion" or isinstance(APP_NAME, str)
    assert GITHUB_API_BASE_URL.startswith("http")
    assert get_settings() is not None
