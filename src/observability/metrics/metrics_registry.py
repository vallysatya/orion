"""In-memory storage for Orion metrics.

MetricsRegistry is the low-level store only:
  - counters (monotonically increasing totals)
  - timings (duration samples in milliseconds)

It does not compute averages, rates, or exports.
MetricsService is the public API that sits on top of this registry.
"""

from __future__ import annotations

from collections import defaultdict
from threading import Lock

from observability.metrics.metrics_snapshot import MetricsSnapshot


class MetricsRegistry:
    """Thread-safe in-memory metrics database."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._timings: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def increment(self, name: str, value: int = 1) -> None:
        """Increase a counter. Value must be non-negative."""
        if value < 0:
            raise ValueError("Counter increment cannot be negative.")

        with self._lock:
            self._counters[name] += value

    def record_timing(self, name: str, duration_ms: float) -> None:
        """Append one duration sample in milliseconds."""
        if duration_ms < 0:
            raise ValueError("Duration cannot be negative.")

        with self._lock:
            self._timings[name].append(duration_ms)

    def get_counter(self, name: str) -> int:
        """Return the current counter value, or 0 if unset."""
        with self._lock:
            return self._counters.get(name, 0)

    def get_timings(self, name: str) -> tuple[float, ...]:
        """Return an immutable copy of timing samples for a name."""
        with self._lock:
            return tuple(self._timings.get(name, []))

    def snapshot(self) -> MetricsSnapshot:
        """Return an immutable copy of all counters and timings."""
        with self._lock:
            return MetricsSnapshot(
                counters=dict(self._counters),
                timings={
                    name: tuple(values)
                    for name, values in self._timings.items()
                },
            )

    def clear(self) -> None:
        """Remove all counters and timing samples."""
        with self._lock:
            self._counters.clear()
            self._timings.clear()
