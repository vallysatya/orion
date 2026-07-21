# Observability

Orion instruments runtime, Guard, memory, tool callbacks, and GitHub with
**in-process** tracing and metrics.

## Tracing

Components:

- `TraceEvent` — timestamped event with component, name, metadata
- `Trace` — ordered event collection
- `TraceService` — `record(...)` API
- Exporters — `ConsoleExporter`, `JsonExporter` (print when explicitly called)

Instrumentation exists for request lifecycle, tool callbacks, guard evaluation,
memory operations, and GitHub HTTP requests.

### Limits

- Process-local; cleared when the process exits
- One shared global `Trace` accumulates across requests (not a per-request span tree)
- Correlation IDs are incomplete for concurrent workloads
- `Trace` itself is not thread-safe
- Exporters are constructed in the container but **not** auto-invoked on every request
- There is intentionally **no** `orion trace` CLI in v1.0

## Metrics

Components:

- `MetricNames` — canonical string constants
- `MetricsRegistry` — thread-safe counters + timing samples
- `MetricsService` — recording helpers + `snapshot()`
- `MetricsSnapshot` — immutable point-in-time DTO

Helpers cover requests, tool allow/block/approval/execution, memory hit/miss/write/delete,
and GitHub request outcomes/durations.

### Limits

- Process-local; no durable backend
- No labels/dimensions (agent, user, status code, …)
- Timing samples grow unbounded in memory
- No histograms/percentiles/exporters beyond snapshot
- There is intentionally **no** `orion metrics` CLI in v1.0

See [Metrics reference](../reference/metrics.md).

## Why CLI commands are deferred

A new process cannot see the previous process's counters or events. Shipping
`orion metrics` / `orion trace` today would look polished but return empty or
misleading data. Durable storage (or a long-lived server) unlocks those commands
in a later release.

## Related docs

- [Architecture](architecture.md)
- [Metrics reference](../reference/metrics.md)
- [Roadmap](../../ROADMAP.md)
