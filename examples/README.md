# Orion examples

Reproducible scenarios that show **what Orion does**, not just what it prints.

Each example includes:

1. The user request or deterministic scenario input
2. Internal flow (`Guard → Memory → Tool → Observability`)
3. Expected output
4. Why the behavior is correct

## Scenarios

| Example | Demonstrates | Deterministic? |
| --- | --- | --- |
| [GitHub issue demo](github_issue_demo.md) | Allowed read-only GitHub request | No — live API + LLM output vary |
| [Safe tool demo](safe_tool_demo.md) | Default `ALLOW` decision | Yes |
| [Blocked PII demo](blocked_pii_demo.md) | PII argument blocking | Yes |
| [Prompt injection demo](prompt_injection_demo.md) | Injection-pattern blocking | Yes |
| [Approval flow demo](approval_flow_demo.md) | `REQUIRE_APPROVAL` classification | Yes |

## Before you begin

```bash
pip install -e ".[dev]"
orion version
orion guard test
```

The four Guard examples are backed by the actual scenarios in
`src/cli/guard_command.py`. The GitHub example uses the real CLI and API, so its
issue data and natural-language answer will change over time.

## Important v1.0 boundaries

- Built-in GitHub tools are **read-only**.
- `create_issue` and `merge_pull_request` in the Guard demos are synthetic
  proposed tool calls used to exercise policies; they are not shipped GitHub
  execution tools.
- `REQUIRE_APPROVAL` skips execution and reports the decision. It is not yet a
  resumable human approval workflow.
- Metrics and traces are process-local; they are described as internal events,
  not shown by a standalone CLI command.

Return to the [main documentation](../docs/README.md).
