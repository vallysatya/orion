# Metrics reference

Canonical names live in `src/observability/metrics/metric_names.py`.
Recording helpers live on `MetricsService`.

## Snapshot

```python
snapshot = metrics_service.snapshot()
# MetricsSnapshot(counters=dict[str, int], timings=dict[str, list[float]])
```

Counters are totals. Timing keys map to lists of millisecond samples.

## Request metrics

| Name | Meaning |
| --- | --- |
| `requests_total` | Requests started |
| `requests_succeeded` | Requests completed successfully |
| `requests_failed` | Requests that failed |
| `request_duration_ms` | Timing samples |

## Tool metrics

| Name | Meaning |
| --- | --- |
| `tool_executions_total` | Tool executions started (allowed path) |
| `tool_executions_succeeded` | Tool executions finished successfully |
| `tool_executions_failed` | Tool executions that failed |
| `tool_calls_allowed` | Guard allow decisions |
| `tool_calls_blocked` | Guard block decisions |
| `tool_calls_approval_required` | Guard approval-required decisions |
| `tool_duration_ms` | Timing samples |

## Memory metrics

| Name | Meaning |
| --- | --- |
| `memory_hits` | Successful reads that found a value |
| `memory_misses` | Reads that found nothing |
| `memory_writes` | Write operations |
| `memory_deletes` | Delete operations |

`MetricsService.memory_hit_rate` derives hit rate from hits/(hits+misses).

## GitHub metrics

| Name | Meaning |
| --- | --- |
| `github_requests_total` | GitHub HTTP requests started |
| `github_requests_succeeded` | Successful GitHub HTTP requests |
| `github_requests_failed` | Failed GitHub HTTP requests |
| `github_request_duration_ms` | Timing samples |

## Helpers

Prefer domain helpers over raw increments when instrumenting:

- `record_request_started/succeeded/failed`
- `record_tool_allowed/blocked/approval_required/started/succeeded/failed`
- `record_memory_hit/miss/write/delete`
- `record_github_request_started/succeeded/failed`

## Limits

- In-process only
- No label dimensions
- Timing lists grow without bound
- No CLI export in v1.0

## Related docs

- [Observability concept](../concepts/observability.md)
- [Architecture](../concepts/architecture.md)
