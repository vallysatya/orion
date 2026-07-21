# Orion

**A guarded, observable multi-agent platform built on Google ADK.**

Orion gives developers a production-minded agent runtime: typed configuration,
policy-enforced tool execution, dual-layer memory, structured errors, and
in-process observability — all accessible through a focused CLI.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Why Orion

Most agent demos wire an LLM to a few tools and stop there. Orion treats the
runtime as a platform:

| Concern | What Orion provides |
| --- | --- |
| **Safety** | Policy-driven Guard evaluates every tool call before execution |
| **Memory** | Session state + durable SQLite preferences |
| **Observability** | Tracing and metrics on requests, tools, memory, and GitHub |
| **Errors** | Typed `OrionError` hierarchy instead of leaking third-party exceptions |
| **Developer UX** | CLI for run, doctor, config, guard, and memory |

```text
You ──► CLI / AgentRunner ──► Coordinator Agent
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
               GitHub Agent   Security Agent   General Agent
                    │
                    ▼
           before_tool_callback
                    │
                    ▼
              GuardService  ──► allow / block / require_approval
                    │
                    ▼
              Tool execution ──► Memory / GitHub / ADK
```

---

## What v1.0 supports

**Shipped and real**

- Interactive and one-shot agent runs (`orion run`)
- Read-only GitHub repository assistant (issues, PRs, releases, contributors, …)
- Guard policies: prompt injection, PII, permissions, environment, destructive actions, approval classification
- Dual memory: ADK session state + SQLite persistence
- In-process tracing and metrics
- Typed configuration with secret redaction
- Developer CLI: `run`, `doctor`, `version`, `help`, `config`, `guard`, `memory`

**Honest boundaries**

- GitHub tools are **read-only** today (no create/merge/delete)
- `REQUIRE_APPROVAL` classifies and skips execution; there is no resumable human-approval workflow yet
- Sessions, traces, and metrics are **process-local** (lost when the process exits)
- SQLite memory is the durable store; conversation history is not persisted across restarts
- Metrics/trace/session/agent/plugin/serve CLI commands are intentionally deferred

Full documentation: **[docs/README.md](docs/README.md)**

---

## Quickstart

### 1. Install

```bash
git clone https://github.com/vallysatya/orion.git
cd orion
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

> Prefer a runtime-only install? Use `pip install .`  
> `pip install -r requirements.txt` installs dependencies only — it does **not** register the `orion` command.

### 2. Configure

```bash
orion config init
copy .env.example .env      # Windows
# cp .env.example .env     # macOS / Linux
```

Edit `.env`:

```bash
GOOGLE_API_KEY=your-google-api-key
GITHUB_TOKEN=your-github-token   # optional for public repos; required for private / authenticated calls
```

### 3. Verify and run

```bash
orion doctor
orion version
orion run "summarize the orion repository"
```

Interactive mode:

```bash
orion run
# You> list my repositories
# You> exit
```

---

## CLI at a glance

```bash
orion run                       # interactive agent session
orion run "list open issues"    # one-shot message
orion doctor                    # health checks
orion config show               # secrets redacted
orion config validate
orion guard status
orion guard test
orion memory stats
orion memory clear --yes
orion version
orion help
```

See the full reference: [docs/reference/cli.md](docs/reference/cli.md)

---

## Architecture

```text
Orion
├── Runtime         AgentRunner + ADK session adapter
├── Agents          Coordinator → GitHub / Security / General
├── Guard           Ordered policy evaluation on every tool call
├── Memory          Session (ADK) + Persistent (SQLite)
├── Observability   TraceService + MetricsService
├── Errors          OrionError hierarchy
├── Config          Typed OrionConfig + ConfigLoader
└── CLI             Developer commands (no placeholders)
```

Deep dive: [docs/concepts/architecture.md](docs/concepts/architecture.md)

---

## Development

```bash
pip install -e ".[dev]"
pytest -q
python -m build
orion version
```

- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Testing: [docs/development/testing.md](docs/development/testing.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Security: [SECURITY.md](SECURITY.md)

---

## Documentation map

| Section | Start here |
| --- | --- |
| Getting started | [Installation](docs/getting-started/installation.md) · [Quickstart](docs/getting-started/quickstart.md) · [Configuration](docs/getting-started/configuration.md) |
| Concepts | [Architecture](docs/concepts/architecture.md) · [Guard](docs/concepts/guard-and-approvals.md) · [Memory](docs/concepts/memory-model.md) · [Observability](docs/concepts/observability.md) |
| Guides | [GitHub assistant](docs/guides/github-assistant.md) · [Security guard](docs/guides/security-guard.md) · [Memory](docs/guides/memory-management.md) · [Troubleshooting](docs/guides/troubleshooting.md) |
| Reference | [CLI](docs/reference/cli.md) · [Config](docs/reference/configuration.md) · [Metrics](docs/reference/metrics.md) · [Errors](docs/reference/errors.md) |
| Development | [Extending](docs/development/extending-orion.md) · [Testing](docs/development/testing.md) · [Releases](docs/development/release-process.md) |

---

## License

MIT — see [LICENSE](LICENSE).
