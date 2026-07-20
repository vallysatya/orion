"""Smoke test for MemoryService + MemoryPolicyEngine wiring."""

from __future__ import annotations

import tempfile
from pathlib import Path

from google.adk.sessions.state import State

from memory.memory_policy_engine import MemoryPolicyEngine
from memory.memory_service import MemoryService
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy
from memory.sqlite_memory import SQLiteMemory
from memory.state_keys import StateKey
from observability.metrics.metrics_registry import MetricsRegistry
from observability.metrics.metrics_service import MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService


def _build_memory(db_path: str) -> tuple[MemoryService, SQLiteMemory]:
    sqlite = SQLiteMemory(database_path=db_path)
    engine = MemoryPolicyEngine(
        policies=[
            DualMemoryPolicy(),
            PersistencePolicy(),
            SessionPolicy(),
        ],
    )
    return MemoryService(
        persistent_memory=sqlite,
        policy_engine=engine,
        trace_service=TraceService(trace=Trace()),
        metrics_service=MetricsService(registry=MetricsRegistry()),
    ), sqlite


class _Ctx:
    def __init__(self) -> None:
        self.state = State({}, {})


def test_policy_routed_memory() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "test_memory.db")
        memory, sqlite = _build_memory(db_path)
        ctx = _Ctx()

        try:
            # Persistent-only preference
            memory.save_preference("user_name", "Sriram")
            assert memory.load_preference("user_name") == "Sriram"

            # Session-only
            memory.set(ctx, StateKey.RISK_SCORE, 90)
            assert memory.get(ctx, StateKey.RISK_SCORE) == 90
            assert memory.load_preference("risk_score") is None

            # BOTH: session + persistent
            # Use raw key via set with a StateKey if present, else preference + session.
            memory.save_preference("default_repository", "orion")
            assert memory.load_preference("default_repository") == "orion"

            # Simulate dual write through set using CURRENT_REPOSITORY as session
            # and verify BOTH key via policy decide path on save_preference.
            from memory.memory_decision import MemoryStorage

            decision = memory._policy_engine.decide(
                "default_repository",
                "orion",
            )
            assert decision.storage == MemoryStorage.BOTH

            print("policy routed memory ok")
        finally:
            sqlite.connection.close()


if __name__ == "__main__":
    test_policy_routed_memory()
