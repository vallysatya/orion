class MetricNames:
    """Canonical metric names used across the Orion platform."""

    # ------------------------------------------------------------------
    # Request metrics
    # ------------------------------------------------------------------
    REQUESTS_TOTAL = "requests_total"
    REQUESTS_SUCCEEDED = "requests_succeeded"
    REQUESTS_FAILED = "requests_failed"

    # ------------------------------------------------------------------
    # Tool execution metrics
    # ------------------------------------------------------------------
    TOOL_EXECUTIONS_TOTAL = "tool_executions_total"
    TOOL_EXECUTIONS_SUCCEEDED = "tool_executions_succeeded"
    TOOL_EXECUTIONS_FAILED = "tool_executions_failed"

    TOOL_CALLS_BLOCKED = "tool_calls_blocked"
    TOOL_CALLS_APPROVAL_REQUIRED = "tool_calls_approval_required"
    TOOL_CALLS_ALLOWED = "tool_calls_allowed"

    # ------------------------------------------------------------------
    # Memory metrics
    # ------------------------------------------------------------------
    MEMORY_HITS = "memory_hits"
    MEMORY_MISSES = "memory_misses"
    MEMORY_WRITES = "memory_writes"
    MEMORY_DELETES = "memory_deletes"

    # ------------------------------------------------------------------
    # GitHub metrics
    # ------------------------------------------------------------------
    GITHUB_REQUESTS_TOTAL = "github_requests_total"
    GITHUB_REQUESTS_SUCCEEDED = "github_requests_succeeded"
    GITHUB_REQUESTS_FAILED = "github_requests_failed"

    # ------------------------------------------------------------------
    # Timing metrics
    # ------------------------------------------------------------------
    REQUEST_DURATION_MS = "request_duration_ms"
    TOOL_DURATION_MS = "tool_duration_ms"
    GITHUB_REQUEST_DURATION_MS = "github_request_duration_ms"
