"""Unit tests for MetricsRegistry (in-memory store)."""

from __future__ import annotations

import pytest

from observability.metrics import MetricNames, MetricsRegistry


def test_registry_stores_counters_and_timings():
    registry = MetricsRegistry()

    registry.increment(MetricNames.REQUESTS_TOTAL)
    registry.record_timing(MetricNames.REQUEST_DURATION_MS, 12.5)

    assert registry.get_counter(MetricNames.REQUESTS_TOTAL) == 1
    assert registry.get_timings(MetricNames.REQUEST_DURATION_MS) == (12.5,)


def test_registry_snapshot_is_a_copy():
    registry = MetricsRegistry()
    registry.increment(MetricNames.TOOL_CALLS_BLOCKED, 2)

    snap = registry.snapshot()
    snap.counters[MetricNames.TOOL_CALLS_BLOCKED] = 99

    assert registry.get_counter(MetricNames.TOOL_CALLS_BLOCKED) == 2
    assert snap.timings == {}


def test_registry_rejects_negative_values():
    registry = MetricsRegistry()

    with pytest.raises(ValueError):
        registry.increment(MetricNames.REQUESTS_TOTAL, -1)

    with pytest.raises(ValueError):
        registry.record_timing(MetricNames.REQUEST_DURATION_MS, -0.1)
