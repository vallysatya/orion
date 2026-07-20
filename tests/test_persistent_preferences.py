"""Smoke test for MemoryService persistent preference helpers."""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_policy_engine import MemoryPolicyEngine
from memory.memory_service import MemoryService
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy
from memory.sqlite_memory import SQLiteMemory
from observability.metrics.metrics_registry import MetricsRegistry
from observability.metrics.metrics_service import MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService


def test_persistent_preferences() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "test_memory.db")
        sqlite = SQLiteMemory(database_path=db_path)
        memory = MemoryService(
            persistent_memory=sqlite,
            policy_engine=MemoryPolicyEngine(
                policies=[
                    DualMemoryPolicy(),
                    PersistencePolicy(),
                    SessionPolicy(),
                ],
            ),
            trace_service=TraceService(trace=Trace()),
            metrics_service=MetricsService(registry=MetricsRegistry()),
        )

        try:
            assert memory.preference_exists("user_name") is False
            assert memory.load_preference("user_name") is None

            memory.save_preference("user_name", "Sriram")
            assert memory.preference_exists("user_name") is True
            assert memory.load_preference("user_name") == "Sriram"

            memory.save_preference("user_name", "Vally")
            assert memory.load_preference("user_name") == "Vally"

            memory.delete_preference("user_name")
            assert memory.preference_exists("user_name") is False
            assert memory.load_preference("user_name") is None

            print("persistent preferences ok")
        finally:
            sqlite.connection.close()


if __name__ == "__main__":
    test_persistent_preferences()
