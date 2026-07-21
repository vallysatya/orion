# Orion Documentation

Welcome to the Orion v1.0 documentation.

Orion is a multi-agent platform built on Google ADK. These docs describe what
is **actually implemented today** — capabilities, workflows, extension seams,
and intentional limitations.

---

## Getting started

| Page | Description |
| --- | --- |
| [Installation](getting-started/installation.md) | Python setup, editable install, packaging |
| [Quickstart](getting-started/quickstart.md) | First successful `orion run` in minutes |
| [Configuration](getting-started/configuration.md) | Environment variables, dotenv, secrets |

## Concepts

| Page | Description |
| --- | --- |
| [Architecture](concepts/architecture.md) | Platform composition and request flow |
| [Agent runtime](concepts/agent-runtime.md) | Agents, sessions, and ADK integration |
| [Guard & approvals](concepts/guard-and-approvals.md) | Policy engine and decision semantics |
| [Memory model](concepts/memory-model.md) | Session vs persistent storage |
| [Observability](concepts/observability.md) | Tracing and metrics (in-process) |

## Guides

| Page | Description |
| --- | --- |
| [GitHub assistant](guides/github-assistant.md) | Read-only repository workflows |
| [Security guard](guides/security-guard.md) | Using and testing Guard |
| [Memory management](guides/memory-management.md) | Preferences, stats, and clearing |
| [Troubleshooting](guides/troubleshooting.md) | Common failures and fixes |

## Reproducible examples

The [examples directory](../examples/README.md) contains presentation-ready
walkthroughs for a live GitHub issue request, a safe tool call, PII blocking,
prompt-injection blocking, and an approval-required decision.

## Reference

| Page | Description |
| --- | --- |
| [CLI](reference/cli.md) | Every command, option, and exit code |
| [Configuration](reference/configuration.md) | Canonical env-var reference |
| [Metrics](reference/metrics.md) | Metric names and snapshot shape |
| [Errors](reference/errors.md) | `OrionError` hierarchy |

## Development

| Page | Description |
| --- | --- |
| [Extending Orion](development/extending-orion.md) | Policies, storage, exporters, agents |
| [Testing](development/testing.md) | Pytest, scripts, caveats |
| [Release process](development/release-process.md) | Versioning, build, verification |

## Project docs (repository root)

| Document | Purpose |
| --- | --- |
| [README.md](../README.md) | Product landing page |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guide |
| [CHANGELOG.md](../CHANGELOG.md) | Release history |
| [ROADMAP.md](../ROADMAP.md) | Future direction |
| [SECURITY.md](../SECURITY.md) | Vulnerability reporting |
| [SUPPORT.md](../SUPPORT.md) | How to get help |
| [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | Community standards |
| [LICENSE](../LICENSE) | MIT license |

---

## Source-of-truth rules

To keep documentation honest and maintainable:

1. **README** — pitch, quickstart, links. No deep reference tables.
2. **CLI reference** — every shipped command and exit code.
3. **Configuration reference** — canonical environment variables.
4. **Architecture / concepts** — lifecycle, ownership, persistence, limits.
5. **CHANGELOG** — what shipped. **ROADMAP** — what might ship next.
6. **Docstrings** — programmatic contracts, not marketing claims.

If a page and the code disagree, trust the code — and open a PR to fix the docs.
