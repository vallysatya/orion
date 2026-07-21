# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 1.0.x | Yes |
| < 1.0 | No |

## Reporting a vulnerability

Please **do not** open a public GitHub Issue for security vulnerabilities.

Use GitHub's private reporting flow:

1. Open the repository on GitHub: [vallysatya/orion](https://github.com/vallysatya/orion)
2. Go to **Security → Advisories → Report a vulnerability**
   (or use the “Report a vulnerability” button if available)
3. Include:
   - affected version / commit
   - impact assessment
   - reproduction steps
   - any known mitigations

We will acknowledge reports as quickly as practical and coordinate a fix and
disclosure timeline.

## Security scope notes (v1.0)

Orion includes deterministic Guard policies and typed error wrapping, but:

- Prompt-injection / PII detection are regex-based and imperfect
- `REQUIRE_APPROVAL` does not yet implement a human resume workflow
- Persistent memory keys are not multi-tenant namespaced
- Sessions/metrics/traces are process-local

When reporting issues, distinguish **implementation bugs** from **documented
v1.0 limitations**.

## Secrets handling

- Never commit `.env` files or tokens
- Prefer `orion config show` (redacted) when sharing configuration state
- Rotate any credential that may have been exposed
