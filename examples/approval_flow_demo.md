# Demo: approval-required decision

## Goal

Demonstrate how Orion classifies a sensitive operation that should require
human approval.

## User request

Synthetic scenario input:

```text
Merge pull request #7.
```

Equivalent proposed call:

```python
tool_name = "merge_pull_request"
arguments = {"number": 7}
environment = "development"
```

`merge_pull_request` is a **synthetic Guard input** in v1.0. Orion does not ship
a mutating GitHub merge tool yet.

## Reproduce

```bash
orion guard test
```

Look for:

```text
✔ Approval Flow
```

The label is retained for CLI compatibility; the implemented behavior is an
**approval-required decision**, not a resumable workflow.

## What Orion does internally

```text
Proposed merge_pull_request
  → PromptInjectionPolicy: no match
  → PIIPolicy: no match
  → PermissionPolicy: no role, so no opinion
  → EnvironmentPolicy: development, so no production rule
  → DestructiveActionPolicy: no match for this name
  → ApprovalPolicy matches merge_pull_request
  → GuardDecision(REQUIRE_APPROVAL, policy="approval_policy")
  → metrics: tool_calls_approval_required += 1
  → trace: PolicyMatched + GuardDecisionMade + ApprovalRequired
  → callback path stores approval_required=true + risk score 60 in session memory
  → callback returns structured result
  → Tool is skipped
```

## Expected output

```text
✔ Approval Flow
```

Structured callback result:

```text
status: require_approval
policy: approval_policy
tool_name: merge_pull_request
reason: The tool 'merge_pull_request' requires human approval before execution.
```

## Why this behavior is correct

- Merge is a sensitive, potentially irreversible repository operation.
- Orion refuses to silently execute it.
- Guard records the decision in memory/observability for downstream reasoning.
- Since v1.0 has no approval store or continuation endpoint, skipping execution
  is safer than pretending approval occurred.

## Current limitation

A human cannot approve and resume this invocation. That workflow belongs on the
roadmap; documentation should not claim it exists today.

See also: [Guard and approvals](../docs/concepts/guard-and-approvals.md).
