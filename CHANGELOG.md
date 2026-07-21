# Changelog

## v1.0.0

First public platform release.

### CLI

- `orion run` — interactive and one-shot agent sessions
- `orion doctor` — configuration and dependency health checks
- `orion version` / `orion help`
- `orion config show|validate|init` — typed config inspection (secrets redacted)
- `orion guard status|test` — policy listing and deterministic guard scenarios
- `orion memory stats|clear` — SQLite persistent-memory inspection

### Platform

- Typed configuration package (`config/`) with secret redaction
- Guard service with policy evaluation and metrics
- Dual memory (session + SQLite) with operation-level error wrapping
- Observability: tracing and metrics integrated into runtime, guard, memory, GitHub client
- Standardized `OrionError` hierarchy across subsystems
- Console script entry point: `orion = cli.main:main`

### Intentionally not in v1.0 CLI

Metrics, trace, session, agent, plugin, and serve commands — deferred until
persistent / out-of-process surfaces exist.

## v0.0.1

- Initialized Orion repository
- Added project structure
