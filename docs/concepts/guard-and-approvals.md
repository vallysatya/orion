# Guard and approvals

Guard is Orion's deterministic safety boundary for tool execution.

## Where it sits

```text
ADK proposes tool
   → before_tool_callback
      → GuardService.evaluate(GuardRequest)
         → GuardDecision(action, reason, policy)
   → allow: execute tool
   → block / require_approval: skip tool, return structured result
   → after_tool_callback (metrics/traces for executed tools)
```

## Policies (default order)

| # | Policy | Typical effect |
| --- | --- | --- |
| 1 | `PromptInjectionPolicy` | Block suspicious instruction-override language in arguments |
| 2 | `PIIPolicy` | Block emails, SSN-like values, keys, private-key blocks, etc. |
| 3 | `PermissionPolicy` | Block tools not allowed for a role (when role is present) |
| 4 | `EnvironmentPolicy` | Stricter block/approval rules in production |
| 5 | `DestructiveActionPolicy` | Block known destructive tool names |
| 6 | `ApprovalPolicy` | Mark sensitive tools as `require_approval` |

First non-`None` decision wins. No match → default `ALLOW` with policy
`default_policy`.

## Decision actions

```text
GuardAction
├── ALLOW
├── BLOCK
└── REQUIRE_APPROVAL
```

### What `REQUIRE_APPROVAL` means in v1.0

- The callback **does not execute** the tool
- A structured result is returned to the agent explaining approval is required
- There is **no** approval store, human confirm UI, or resume/retry workflow

Document and product language should say “approval-required decision,” not
“human approval flow,” until a continuation mechanism exists.

## Request shape

`GuardRequest` includes request id, user id, session id, tool name, arguments,
optional agent name, and environment.

Current callback behavior:

- Uses ADK invocation id when available
- Sets `user_id` / `session_id` placeholders (`unknown-user` / `unknown-session`)
- Reads remembered environment from memory when available
- Does not currently attach `user_role`, so `PermissionPolicy` often no-ops

## Detection limits

Prompt-injection and PII checks are **regex scans of serialized arguments**.
They can false-positive, do not inspect full chat context, and do not scan tool
outputs.

## Observability

Guard emits trace events such as `GuardCheckRequested`, `PolicyMatched`,
`GuardDecisionMade`, `Allowed`, `Blocked`, and `ApprovalRequired`, and updates
metrics for allowed / blocked / approval-required counts.

## Testing

```bash
orion guard status
orion guard test
```

## Extending

Implement `BasePolicy.evaluate(request) -> GuardDecision | None` and insert it
into the ordered policy list used by `build_guard_policies()` /
`GuardService`. See [Extending Orion](../development/extending-orion.md).

## Related docs

- [Security guard guide](../guides/security-guard.md)
- [Architecture](architecture.md)
- [Metrics](../reference/metrics.md)
