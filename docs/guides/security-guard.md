# Security guard guide

Orion's Guard evaluates every tool call **before** ADK executes it. This page
covers day-to-day usage. For internals, see
[Guard & approvals](../concepts/guard-and-approvals.md).

## Inspect loaded policies

```bash
orion guard status
```

Default policy order:

1. `PromptInjectionPolicy`
2. `PIIPolicy`
3. `PermissionPolicy`
4. `EnvironmentPolicy`
5. `DestructiveActionPolicy`
6. `ApprovalPolicy`

Evaluation is **first match wins**. If no policy returns a decision, Guard
defaults to `ALLOW`.

## Run deterministic scenarios

```bash
orion guard test
```

Built-in scenarios:

| Scenario | Expected decision |
| --- | --- |
| Safe Tool Call | `allow` |
| PII Detection | `block` |
| Prompt Injection Detection | `block` |
| Approval Flow | `require_approval` |

Exit code `0` means all scenarios passed; `1` means at least one failed.

## Decisions you will see

| Action | Meaning in v1.0 |
| --- | --- |
| `allow` | Tool may execute |
| `block` | Tool is skipped; structured block result returned to the agent |
| `require_approval` | Tool is skipped; structured “approval required” result returned |

Important: `require_approval` is a **classification**, not a resumable human
workflow. There is no approval queue, confirm endpoint, or retry/resume path in
v1.0.

## What Guard scans

Prompt-injection and PII policies inspect **serialized tool arguments** with
regex patterns. They do not scan the full model conversation or tool outputs.

This can produce false positives. Prefer clean arguments and review blocks in
agent responses when unexpected.

## Permission and environment notes

- Role-based `PermissionPolicy` only acts when a `user_role` is present on the
  request. The default callback path currently does not supply a role, so the
  policy often has “no opinion.”
- `EnvironmentPolicy` tightens controls when the remembered environment is
  `production` / `prod`.

## Observability

Guard records traces and metrics for:

- check requested / policy matched / decision made
- allowed, blocked, and approval-required counts

These counters are process-local. There is no `orion metrics` command yet.

## Related docs

- [Guard & approvals concept](../concepts/guard-and-approvals.md)
- [CLI reference](../reference/cli.md)
- [Extending Orion](../development/extending-orion.md)
