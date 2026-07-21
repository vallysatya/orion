# Demo: block PII in tool arguments

## Goal

Show Orion preventing a proposed tool call from carrying personally identifiable
information into an external integration.

## User request

Synthetic scenario input:

```text
Create an issue whose body says: "contact me at jane.doe@example.com"
```

Equivalent proposed call:

```python
tool_name = "create_issue"
arguments = {"body": "contact me at jane.doe@example.com"}
```

`create_issue` is a **synthetic Guard input** in v1.0. Orion's built-in GitHub
surface is read-only and does not expose issue creation.

## Reproduce

```bash
orion guard test
```

Look for:

```text
✔ PII Detection
```

## What Orion does internally

```text
Proposed tool arguments
  → PromptInjectionPolicy: no match
  → PIIPolicy serializes arguments to JSON
  → email_address regex matches jane.doe@example.com
  → GuardDecision(BLOCK, policy="pii_policy")
  → metrics: tool_calls_blocked += 1
  → trace: PolicyMatched + GuardDecisionMade + Blocked
  → callback path stores decision + risk score 100 in session memory
  → callback returns structured block result
  → Tool is skipped (no GitHub request)
  → no tool-execution success metric is recorded
```

Observability records the policy outcome; it must not record the sensitive
argument value in the decision metadata.

## Expected output

The deterministic CLI output is:

```text
✔ PII Detection
```

The callback's structured result would be:

```text
status: block
policy: pii_policy
tool_name: create_issue
reason: Possible email address detected in arguments for tool 'create_issue'.
```

## Why this behavior is correct

- The email appears in tool arguments and matches a configured PII pattern.
- First-match-wins stops evaluation at `PIIPolicy`.
- Blocking occurs before any external tool or HTTP client runs.
- Session memory records only security context (decision/risk), while the
  proposed PII is not deliberately persisted by this flow.

## Limits

PII detection is regex-based. It can produce false positives and does not scan
the full conversation or tool output.

See also: [Security guard guide](../docs/guides/security-guard.md).
