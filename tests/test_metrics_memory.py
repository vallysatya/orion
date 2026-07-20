from memory.memory_policy_engine import MemoryPolicyEngine
from memory.memory_service import MemoryService
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy
from memory.sqlite_memory import SQLiteMemory
from observability.metrics import MetricNames, MetricsRegistry, MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService


class _Ctx:
    def __init__(self) -> None:
        self.state: dict = {}


def test_memory_hit_and_miss_metrics(tmp_path):
    metrics = MetricsService(registry=MetricsRegistry())
    memory = MemoryService(
        persistent_memory=SQLiteMemory(
            database_path=str(tmp_path / "metrics_memory.db"),
        ),
        policy_engine=MemoryPolicyEngine(
            policies=[
                DualMemoryPolicy(),
                PersistencePolicy(),
                SessionPolicy(),
            ],
        ),
        trace_service=TraceService(trace=Trace()),
        metrics_service=metrics,
    )
    ctx = _Ctx()

    assert memory.get(ctx, "missing_key") is None
    assert metrics.get_counter(MetricNames.MEMORY_MISSES) == 1

    memory.set(ctx, "risk_score", 42)
    assert metrics.get_counter(MetricNames.MEMORY_WRITES) == 1
    assert memory.get(ctx, "risk_score") == 42
    assert metrics.get_counter(MetricNames.MEMORY_HITS) == 1
    assert metrics.memory_hit_rate() == 0.5

    memory.delete(ctx, "risk_score")
    assert metrics.get_counter(MetricNames.MEMORY_DELETES) == 1
