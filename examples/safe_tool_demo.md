# Demo: safe tool call

## Goal

Demonstrate the default allowed path for a harmless tool request.

## User request

Conceptually:

```text
Get repository information for orion/orion.
```

The deterministic Guard harness represents it as:

```python
tool_name = "get_repository"
arguments = {"owner": "orion", "repo": "orion"}
environment = "development"
```

> The scenario tests Guard only. The built-in live wrapper is named
> `get_repository_info`; both names receive the same default-allow behavior
> because no blocking policy matches.

## Reproduce

```bash
orion guard test
```

Look for:

```text
✔ Safe Tool Call
```

(`PASS Safe Tool Call` is the equivalent ASCII fallback.)

## What Orion does internally

```text
GuardScenario
  → build_guard_service creates isolated Trace + Metrics services
  → GuardRequest is created
  → GuardService records GuardCheckRequested
  → policies evaluate in order
  → no policy returns a decision
  → default_policy returns ALLOW
  → metrics: tool_calls_allowed += 1
  → trace: GuardDecisionMade + Allowed
```

In a real ADK tool call, `before_tool_callback` also reads the environment from
MemoryService, stores the last decision/risk in session memory, starts execution
metrics, and returns `None` so the tool runs. `after_tool_callback` then records
success/failure and duration.

## Expected output

```text
✔ Safe Tool Call
```

Decision details:

```text
action: allow
policy: default_policy
reason: Tool execution allowed.
risk score in callback path: 10
```

## Why this behavior is correct

- The request contains no PII or injection language.
- It does not match a production restriction, destructive action, or approval
  tool name.
- Guard is fail-closed for matched threats but defaults to allow when every
  policy explicitly has no opinion.
- The deterministic CLI check does not make a network request.

See also: [Guard and approvals](../docs/concepts/guard-and-approvals.md).
