"""Public interface for recording and reading Orion metrics."""

from __future__ import annotations

from observability.metrics.metric_names import MetricNames
from observability.metrics.metrics_registry import MetricsRegistry
from observability.metrics.metrics_snapshot import MetricsSnapshot


class MetricsService:
    """Public interface for recording and reading Orion metrics."""

    def __init__(self, registry: MetricsRegistry) -> None:
        self._registry = registry

    def increment(self, name: str, value: int = 1) -> None:
        self._registry.increment(name, value)

    def record_timing(self, name: str, duration_ms: float) -> None:
        self._registry.record_timing(name, duration_ms)

    def get_counter(self, name: str) -> int:
        return self._registry.get_counter(name)

    def get_timings(self, name: str) -> tuple[float, ...]:
        return self._registry.get_timings(name)

    def get_average_timing(self, name: str) -> float:
        timings = self._registry.get_timings(name)

        if not timings:
            return 0.0

        return sum(timings) / len(timings)

    def memory_hit_rate(self) -> float:
        """Return hits / (hits + misses), or 0.0 when no reads yet."""
        hits = self.get_counter(MetricNames.MEMORY_HITS)
        misses = self.get_counter(MetricNames.MEMORY_MISSES)
        total = hits + misses
        if total == 0:
            return 0.0
        return hits / total

    def snapshot(self) -> MetricsSnapshot:
        return self._registry.snapshot()

    def clear(self) -> None:
        self._registry.clear()

    # ------------------------------------------------------------------
    # Request helpers
    # ------------------------------------------------------------------

    def record_request_started(self) -> None:
        self.increment(MetricNames.REQUESTS_TOTAL)

    def record_request_succeeded(self, duration_ms: float) -> None:
        self.increment(MetricNames.REQUESTS_SUCCEEDED)
        self.record_timing(MetricNames.REQUEST_DURATION_MS, duration_ms)

    def record_request_failed(self, duration_ms: float) -> None:
        self.increment(MetricNames.REQUESTS_FAILED)
        self.record_timing(MetricNames.REQUEST_DURATION_MS, duration_ms)

    # ------------------------------------------------------------------
    # Guard / tool-policy helpers
    # ------------------------------------------------------------------

    def record_tool_allowed(self) -> None:
        self.increment(MetricNames.TOOL_CALLS_ALLOWED)

    def record_tool_blocked(self) -> None:
        self.increment(MetricNames.TOOL_CALLS_BLOCKED)

    def record_tool_approval_required(self) -> None:
        self.increment(MetricNames.TOOL_CALLS_APPROVAL_REQUIRED)

    # ------------------------------------------------------------------
    # Tool runtime helpers
    # ------------------------------------------------------------------

    def record_tool_started(self) -> None:
        self.increment(MetricNames.TOOL_EXECUTIONS_TOTAL)

    def record_tool_succeeded(self, duration_ms: float | None = None) -> None:
        self.increment(MetricNames.TOOL_EXECUTIONS_SUCCEEDED)
        if duration_ms is not None:
            self.record_timing(MetricNames.TOOL_DURATION_MS, duration_ms)

    def record_tool_failed(self, duration_ms: float | None = None) -> None:
        self.increment(MetricNames.TOOL_EXECUTIONS_FAILED)
        if duration_ms is not None:
            self.record_timing(MetricNames.TOOL_DURATION_MS, duration_ms)

    # ------------------------------------------------------------------
    # Memory helpers
    # ------------------------------------------------------------------

    def record_memory_hit(self) -> None:
        self.increment(MetricNames.MEMORY_HITS)

    def record_memory_miss(self) -> None:
        self.increment(MetricNames.MEMORY_MISSES)

    def record_memory_write(self) -> None:
        self.increment(MetricNames.MEMORY_WRITES)

    def record_memory_delete(self) -> None:
        self.increment(MetricNames.MEMORY_DELETES)

    # ------------------------------------------------------------------
    # GitHub helpers
    # ------------------------------------------------------------------

    def record_github_request_started(self) -> None:
        self.increment(MetricNames.GITHUB_REQUESTS_TOTAL)

    def record_github_request_succeeded(self, duration_ms: float) -> None:
        self.increment(MetricNames.GITHUB_REQUESTS_SUCCEEDED)
        self.record_timing(
            MetricNames.GITHUB_REQUEST_DURATION_MS,
            duration_ms,
        )

    def record_github_request_failed(self, duration_ms: float) -> None:
        self.increment(MetricNames.GITHUB_REQUESTS_FAILED)
        self.record_timing(
            MetricNames.GITHUB_REQUEST_DURATION_MS,
            duration_ms,
        )
