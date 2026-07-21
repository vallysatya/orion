# Errors reference

All Orion-specific failures inherit from `OrionError`.

```text
OrionError
├── OrionRuntimeError
├── GuardError
│   └── GuardEvaluationError
├── ToolExecutionError
├── OrionMemoryError
│   └── MemoryOperationError
├── IntegrationError
│   └── GitHubIntegrationError
└── ConfigurationError
```

> Note: the memory base class is named `OrionMemoryError` to avoid clashing with
> Python's built-in `MemoryError`.

## Common attributes

| Error | Useful fields |
| --- | --- |
| `OrionRuntimeError` | `operation`, `session_id` |
| `GuardEvaluationError` | `tool_name`, `policy` |
| `ToolExecutionError` | `tool_name` |
| `MemoryOperationError` | `operation`, `key` |
| `GitHubIntegrationError` | `operation`, `method`, `endpoint`, `status_code` |
| `ConfigurationError` | `setting` |

Original exceptions are preserved via `raise ... from exc` where applicable.

## Where they are raised

| Subsystem | Typical wrap |
| --- | --- |
| AgentRunner | unexpected failures → `OrionRuntimeError` |
| GuardService | policy failures → `GuardEvaluationError` |
| Tool callback | unexpected before-callback failures → `ToolExecutionError` |
| SQLiteMemory | sqlite/JSON/type errors → `MemoryOperationError` |
| GitHubClient | HTTP/transport errors → `GitHubIntegrationError` |
| Config validation/loader | invalid settings → `ConfigurationError` |

## CLI behavior

Top-level CLI catches `OrionError` and prints:

```text
[ErrorClassName] message
```

Interactive `orion run` prints message-level Orion errors and continues the
session. Unexpected non-Orion exceptions may still produce tracebacks.

## Related docs

- [Architecture](../concepts/architecture.md)
- [Troubleshooting](../guides/troubleshooting.md)
