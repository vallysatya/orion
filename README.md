# Orion

Orion is a multi-agent platform built on Google ADK, with a shared runtime,
typed configuration, persistent memory, a policy-driven security guard, and
first-class observability (tracing + metrics).

**Version:** 1.0.0

---

## Platform

```text
Orion
├── Runtime        AgentRunner + session management
├── Memory         Dual memory (session + SQLite)
├── Guard          Policy engine for tool safety
├── Observability  Tracing + metrics
├── Errors         Typed error hierarchy
├── Config         Typed configuration package
└── CLI            Developer commands
```

---

## Install

```bash
cd orion
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -e .
# or
pip install -r requirements.txt
```

Copy the sample environment file and fill in secrets:

```bash
orion config init
# then copy .env.example → .env and edit
```

Required for agent runs:

- `GOOGLE_API_KEY`
- `GITHUB_TOKEN` (for authenticated GitHub operations)

---

## CLI (v1.0)

Orion ships a focused CLI. Every command is backed by real implementation —
no placeholders.

### Core

| Command         | Purpose                              |
| --------------- | ------------------------------------ |
| `orion run`     | Start interactive chat (or one-shot) |
| `orion doctor`  | Check configuration and dependencies |
| `orion version` | Print version                        |
| `orion help`    | Show all commands                    |

```bash
orion run
orion run "list my repositories"
orion doctor
orion version
```

### Configuration

| Command                 | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `orion config show`     | Display config (secrets redacted)            |
| `orion config validate` | Validate typed configuration                 |
| `orion config init`     | Write a sample `.env.example`                |

```bash
orion config show
orion config validate
orion config init --path .env.example
orion config init --force   # overwrite existing template
```

### Guard

| Command              | Purpose                               |
| -------------------- | ------------------------------------- |
| `orion guard status` | List loaded security policies         |
| `orion guard test`   | Run deterministic sample evaluations  |

```bash
orion guard status
orion guard test
```

Example `guard test` output:

```text
✔ Safe Tool Call
✔ PII Detection
✔ Prompt Injection Detection
✔ Approval Flow
```

### Memory

| Command               | Purpose                         |
| --------------------- | ------------------------------- |
| `orion memory stats`  | Show database path, entries, size |
| `orion memory clear`  | Clear persistent memory         |

```bash
orion memory stats
orion memory clear --yes
```

---

## Intentionally deferred (v1.1+)

These subsystems exist inside the process, but do not yet have durable
out-of-process surfaces suitable for a standalone CLI:

- `orion metrics`
- `orion trace`
- `orion session`
- `orion agent`
- `orion plugin`
- `orion serve`

Shipping them now would create commands that look complete but cannot
reliably produce meaningful output in a new process.

---

## Architecture highlights

- **Typed config** — `OrionConfig` with `GitHubConfig`, `RuntimeConfig`,
  `MemoryConfig`; secrets never appear in `repr`, errors, or CLI output.
- **Guard policies** — prompt injection, PII, permissions, environment,
  destructive actions, and approval gates.
- **Error model** — `OrionError` hierarchy (`GitHubIntegrationError`,
  `MemoryOperationError`, `GuardEvaluationError`, …).
- **Observability** — in-process tracing and metrics wired into runtime,
  guard, memory, and GitHub client.

---

## Development

```bash
cd orion
$env:PYTHONPATH = "src"   # Windows PowerShell
pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

---

## License

See [LICENSE](LICENSE).
