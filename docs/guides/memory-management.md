# Memory management

Orion uses a dual-memory model:

| Layer | Backend | Lifetime |
| --- | --- | --- |
| Session | ADK `ToolContext.state` | Process / conversation |
| Persistent | SQLite (`ORION_MEMORY_DB`) | Survives restarts |

Concept deep-dive: [Memory model](../concepts/memory-model.md)

## Inspect persistent memory

```bash
orion memory stats
```

Example output:

```text
Database : C:\...\orion\orion_memory.db
Entries  : 3
Size     : 12.0 KB
```

Side effect: opening the SQLite backend creates the database file and table if
they do not exist.

## Clear persistent memory

```bash
orion memory clear --yes
```

Without `--yes`, Orion refuses:

```text
Refusing to clear memory without confirmation. Pass --yes.
```

Clearing removes **all** persistent entries (global keys), not one user's data.
Session state is unaffected until the process ends.

## What gets stored where

| Keys | Storage |
| --- | --- |
| `user_name`, `preferred_language`, `explanation_style` | Persistent only |
| `default_repository` | Both (dual) |
| Repository / security / environment context keys | Session only |
| Unknown keys | Session only (default) |

Persistent keys are **not namespaced by user**. Prefer single-operator local
use in v1.0, or treat the SQLite file as a private local store.

## Configuration

```bash
ORION_MEMORY_DB=C:\path\to\custom.db
```

Empty / unset → `<project-root>/orion_memory.db`.

## Agent-facing tools

Agents expose memory tools for preferences, repository context, and security
context. Those tools still pass through Guard before execution.

## Safety tips

1. Do not store secrets in memory — agent prompts discourage it, and Guard may
   block PII-like argument content.
2. Back up or relocate `ORION_MEMORY_DB` if preferences matter.
3. Use `orion memory clear --yes` only when intentional.

## Related docs

- [Memory model](../concepts/memory-model.md)
- [CLI reference](../reference/cli.md)
- [Troubleshooting](troubleshooting.md)
