# Changelog

All notable changes to Orion are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Comprehensive Markdown documentation set under `docs/`
- Project governance docs: `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`
- Expanded `CONTRIBUTING.md`

### Changed

- Root `README.md` rewritten as a concise product landing page with honest v1.0 boundaries
- `ROADMAP.md` focused on future work only

## [1.0.0] - 2026-07-20

First public platform release.

### Added

#### CLI

- `orion run` — interactive and one-shot agent sessions
- `orion doctor` — configuration and dependency health checks
- `orion version` / `orion help`
- `orion config show|validate|init` — typed config inspection (secrets redacted)
- `orion guard status|test` — policy listing and deterministic guard scenarios
- `orion memory stats|clear` — SQLite persistent-memory inspection

#### Platform

- Typed configuration package (`src/config/`) with secret redaction
- Guard service with ordered policy evaluation and metrics
- Dual memory (ADK session + SQLite) with operation-level error wrapping
- Observability: tracing and metrics integrated into runtime, guard, memory, and GitHub client
- Standardized `OrionError` hierarchy across subsystems
- setuptools packaging (`src` layout) and console script `orion = cli.main:main`

### Notes

Metrics, trace, session, agent, plugin, and serve CLI commands were intentionally
deferred until durable / out-of-process surfaces exist.

## [0.0.1] - 2026-06-01

### Added

- Initialized Orion repository
- Added project structure

[Unreleased]: https://github.com/vallysatya/orion/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vallysatya/orion/releases/tag/v1.0.0
[0.0.1]: https://github.com/vallysatya/orion/releases/tag/v0.0.1
