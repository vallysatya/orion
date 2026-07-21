# Orion Roadmap

This document describes **future direction**. Completed work belongs in
[CHANGELOG.md](CHANGELOG.md) and the current product surface belongs in
[README.md](README.md) / [docs/](docs/README.md).

## Near term (v1.1)

Focused on making already-built subsystems operable across processes:

- Durable metrics storage and a truthful `orion metrics` command
- Durable / exportable traces and a truthful `orion trace` command
- Persistent sessions and session CLI (`list` / `clear` / `export`)
- Human approval continuation for `REQUIRE_APPROVAL` decisions
- Wire remembered `user_role` into Guard requests so permission policy is active
- Close shared resources cleanly on app shutdown (SQLite, HTTP client)

## Medium term (v1.2 – v2.0)

- Mutating GitHub tools behind Guard + approval gates
- `orion serve` HTTP/API surface
- Agent / tool listing commands backed by a real registry
- Plugin discovery mechanism (replace ad-hoc extension seams)
- Optional dashboard for metrics, traces, and guard decisions
- Multi-user / namespaced persistent memory

## Exploratory

- Broader multi-agent orchestration patterns
- Plugin marketplace
- Additional model providers beyond the current ADK/Gemini wiring
- Stronger reproducibility (pinned dependency sets / lockfiles)

## Non-goals for now

- Shipping placeholder CLI commands that cannot produce meaningful output
- Claiming multi-tenant security properties without namespaced memory and authn/z
- Treating regex Guard policies as a complete security boundary

## How to influence the roadmap

Open a GitHub Issue or Discussion with a concrete use case. Security-sensitive
proposals should follow [SECURITY.md](SECURITY.md).
