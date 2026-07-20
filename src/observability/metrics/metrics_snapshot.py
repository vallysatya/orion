"""Immutable metrics DTO returned by MetricsService.snapshot()."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricsSnapshot:
    """
    Point-in-time view of Orion metrics.

    Immutable and typed so callers cannot mutate live registry state,
    and so we can extend later (percentiles, rates, labels) cleanly.
    """

    counters: dict[str, int]
    timings: dict[str, tuple[float, ...]]
