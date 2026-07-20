"""Focused automated tests for the Orion Memory Engine."""

from __future__ import annotations

from memory.memory_policy_engine import MemoryPolicyEngine
from memory.memory_service import MemoryService
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy
from memory.sqlite_memory import SQLiteMemory


class FakeToolContext:
    def __init__(self) -> None:
        self.state: dict = {}


def create_memory_service(tmp_path):
    database_path = tmp_path / "test_orion_memory.db"

    persistent_memory = SQLiteMemory(
        database_path=str(database_path),
    )

    policy_engine = MemoryPolicyEngine(
        policies=[
            DualMemoryPolicy(),
            PersistencePolicy(),
            SessionPolicy(),
        ]
    )

    memory_service = MemoryService(
        persistent_memory=persistent_memory,
        policy_engine=policy_engine,
    )

    return memory_service, persistent_memory


def test_session_key_is_stored_only_in_session(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    memory_service.set(
        tool_context=tool_context,
        key="risk_score",
        value=90,
    )

    assert tool_context.state["risk_score"] == 90
    assert persistent_memory.exists("risk_score") is False


def test_persistent_key_is_stored_only_in_sqlite(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    memory_service.set(
        tool_context=tool_context,
        key="user_name",
        value="Sriram",
    )

    assert persistent_memory.get("user_name") == "Sriram"
    assert "user_name" not in tool_context.state


def test_dual_key_is_stored_in_both_locations(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    memory_service.set(
        tool_context=tool_context,
        key="default_repository",
        value="orion",
    )

    assert tool_context.state["default_repository"] == "orion"
    assert persistent_memory.get("default_repository") == "orion"


def test_get_hydrates_session_from_sqlite(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    persistent_memory.set("user_name", "Sriram")
    assert "user_name" not in tool_context.state

    value = memory_service.get(
        tool_context=tool_context,
        key="user_name",
    )

    assert value == "Sriram"
    assert tool_context.state["user_name"] == "Sriram"


def test_get_prefers_session_value_over_sqlite(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    persistent_memory.set("user_name", "Old Name")
    tool_context.state["user_name"] = "Current Name"

    value = memory_service.get(
        tool_context=tool_context,
        key="user_name",
    )

    assert value == "Current Name"


def test_delete_removes_session_key_only(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    tool_context.state["risk_score"] = 90

    memory_service.delete(
        tool_context=tool_context,
        key="risk_score",
    )

    assert "risk_score" not in tool_context.state
    assert persistent_memory.exists("risk_score") is False


def test_delete_removes_persistent_key(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    persistent_memory.set("user_name", "Sriram")

    memory_service.delete(
        tool_context=tool_context,
        key="user_name",
    )

    assert persistent_memory.exists("user_name") is False


def test_delete_removes_dual_key_from_both_locations(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    tool_context.state["default_repository"] = "orion"
    persistent_memory.set("default_repository", "orion")

    memory_service.delete(
        tool_context=tool_context,
        key="default_repository",
    )

    assert "default_repository" not in tool_context.state
    assert persistent_memory.exists("default_repository") is False


def test_unknown_key_defaults_to_session_storage(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    memory_service.set(
        tool_context=tool_context,
        key="temporary_note",
        value="hello",
    )

    assert tool_context.state["temporary_note"] == "hello"
    assert persistent_memory.exists("temporary_note") is False


def test_exists_checks_persistent_memory(tmp_path):
    memory_service, persistent_memory = create_memory_service(tmp_path)
    tool_context = FakeToolContext()

    persistent_memory.set("preferred_language", "English")

    result = memory_service.exists(
        tool_context=tool_context,
        key="preferred_language",
    )

    # exists() checks SQLite without hydrating session.
    assert result is True
    assert "preferred_language" not in tool_context.state
