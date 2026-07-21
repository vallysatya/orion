"""Focused tests for Orion's developer CLI."""

from __future__ import annotations

from types import SimpleNamespace

from cli.config_command import run_config
from cli.doctor_command import run_doctor
from cli.guard_command import run_guard
from cli.main import main
from cli.memory_command import run_memory
from cli.version_command import run_version
from config import GitHubConfig, MemoryConfig, OrionConfig, RuntimeConfig
from memory.sqlite_memory import SQLiteMemory


class _FakePersistentMemory:
    def __init__(self, repository: str | None = "owner/repo") -> None:
        self._repository = repository

    def get(self, key: str):
        if key in {"default_repository", "current_repository"}:
            return self._repository
        return None

    def exists(self, key: str) -> bool:
        return False


def _settings(
    *,
    token: str | None = "test-token",
    google_api_key: str | None = "test-api-key",
) -> OrionConfig:
    return OrionConfig(
        github=GitHubConfig(token=token),
        runtime=RuntimeConfig(google_api_key=google_api_key),
        memory=MemoryConfig(database_path="test.db"),
    )


def test_version_prints_public_version(capsys):
    assert run_version() == 0
    assert capsys.readouterr().out.strip() == "Orion 1.0.1"


def test_main_dispatches_version(capsys):
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == "Orion 1.0.1"


def test_main_dispatches_run_message(monkeypatch):
    received: list[str | None] = []
    monkeypatch.setattr(
        "cli.main.run_orion",
        lambda message=None: received.append(message) or 0,
    )

    assert main(["run", "show", "my", "repositories"]) == 0
    assert received == ["show my repositories"]


def test_doctor_returns_zero_when_all_checks_pass(capsys):
    fake_container = SimpleNamespace(
        persistent_memory=_FakePersistentMemory(),
    )

    assert (
        run_doctor(
            settings=_settings(),
            app_container=fake_container,
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "GitHub token configured" in output
    assert "Repository configured" in output
    assert "Memory database available" in output
    assert "Model/API configuration valid" in output
    assert "OK" in output or "✓" in output


def test_doctor_returns_one_for_missing_configuration(capsys):
    fake_container = SimpleNamespace(
        persistent_memory=_FakePersistentMemory(repository=None),
    )

    assert (
        run_doctor(
            settings=_settings(token=None, google_api_key=None),
            app_container=fake_container,
        )
        == 1
    )
    output = capsys.readouterr().out
    assert "GitHub token configured" in output
    assert "Repository configured" in output
    assert "Memory database available" in output
    assert "Model/API configuration valid" in output
    assert "test-token" not in output


# --- config commands ---------------------------------------------------


def test_config_show_redacts_secrets(capsys):
    assert run_config("show", settings=_settings()) == 0
    output = capsys.readouterr().out
    assert "App name" in output
    assert "********" in output
    assert "test-token" not in output
    assert "test-api-key" not in output


def test_config_validate_reports_success(capsys):
    assert run_config("validate", settings=_settings()) == 0
    assert "Configuration is valid" in capsys.readouterr().out


def test_config_validate_reports_failure(capsys):
    broken = OrionConfig(
        github=GitHubConfig(api_base_url="ftp://bad"),
        runtime=RuntimeConfig(),
        memory=MemoryConfig(database_path="test.db"),
    )
    assert run_config("validate", settings=broken) == 1
    assert "Invalid configuration" in capsys.readouterr().out


def test_config_init_writes_template(tmp_path, capsys):
    target = tmp_path / ".env.example"
    assert run_config("init", target=target) == 0
    assert target.exists()
    assert "GITHUB_TOKEN=" in target.read_text(encoding="utf-8")


def test_config_init_refuses_to_overwrite(tmp_path, capsys):
    target = tmp_path / ".env.example"
    target.write_text("existing", encoding="utf-8")
    assert run_config("init", target=target) == 1
    assert target.read_text(encoding="utf-8") == "existing"


def test_config_init_force_overwrites(tmp_path):
    target = tmp_path / ".env.example"
    target.write_text("existing", encoding="utf-8")
    assert run_config("init", target=target, force=True) == 0
    assert "GITHUB_TOKEN=" in target.read_text(encoding="utf-8")


# --- guard commands ----------------------------------------------------


def test_guard_status_lists_policies(capsys):
    assert run_guard("status") == 0
    output = capsys.readouterr().out
    assert "Guard policies" in output
    assert "PIIPolicy" in output


def test_guard_test_all_scenarios_pass(capsys):
    assert run_guard("test") == 0
    output = capsys.readouterr().out
    assert "Safe Tool Call" in output
    assert "PII Detection" in output
    assert "Prompt Injection Detection" in output
    assert "Approval Flow" in output


# --- memory commands ---------------------------------------------------


def test_memory_stats_reports_entries(tmp_path, capsys):
    db_path = str(tmp_path / "mem.db")
    memory = SQLiteMemory(database_path=db_path)
    memory.set("alpha", 1)
    memory.set("beta", 2)

    assert run_memory("stats", memory=memory, database_path=db_path) == 0
    output = capsys.readouterr().out
    assert "Entries" in output
    assert "2" in output


def test_memory_clear_requires_confirmation(tmp_path, capsys):
    db_path = str(tmp_path / "mem.db")
    memory = SQLiteMemory(database_path=db_path)
    memory.set("alpha", 1)

    assert run_memory("clear", memory=memory, database_path=db_path) == 1
    assert memory.count() == 1


def test_memory_clear_with_confirmation(tmp_path, capsys):
    db_path = str(tmp_path / "mem.db")
    memory = SQLiteMemory(database_path=db_path)
    memory.set("alpha", 1)
    memory.set("beta", 2)

    assert (
        run_memory("clear", memory=memory, database_path=db_path, confirm=True)
        == 0
    )
    assert memory.count() == 0


def test_main_dispatches_guard_test():
    assert main(["guard", "test"]) == 0
