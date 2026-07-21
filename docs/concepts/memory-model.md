# Memory model

Orion routes memory writes through a policy engine that decides **session**,
**persistent**, or **both**.

## Layers

```text
MemoryService
├── ADK session state     (fast, process-local)
└── PersistentMemory
      └── SQLiteMemory    (durable key/value JSON)
```

## Routing policies

Configured in the application container (order matters):

1. `DualMemoryPolicy` — keys stored in both layers
2. `PersistencePolicy` — SQLite only
3. `SessionPolicy` — session only

Unknown keys default to session storage.

### Key map (v1.0)

| Category | Examples | Storage |
| --- | --- | --- |
| User preferences | `user_name`, `preferred_language`, `explanation_style` | Persistent |
| Dual | `default_repository` | Both |
| Repo / security context | `current_repository`, `environment`, `risk_score`, … | Session |

## Read path

1. Check session state
2. On miss, read SQLite
3. If found in SQLite, hydrate into session
4. Record hit/miss metrics and traces

Persistent preference writes may not appear in session until a later read
hydrates them.

## Write / delete path

1. Ask `MemoryPolicyEngine` for a `MemoryDecision`
2. Apply to session, SQLite, or both
3. Record write/delete metrics and traces

Values written to SQLite must be JSON-serializable. Failures become
`MemoryOperationError`.

## Scope and multi-user reality

Persistent keys are **global** (not scoped by user/tenant). Treat the SQLite
file as a single-operator local store unless you add namespacing yourself.

## CLI

```bash
orion memory stats
orion memory clear --yes
```

`stats` / opening the DB can create the file. `clear` wipes all persistent rows.

## What memory is not

- Not a durable chat log
- Not a vector store
- Not a multi-tenant preference service (yet)

## Related docs

- [Memory management guide](../guides/memory-management.md)
- [Architecture](architecture.md)
- [Extending Orion](../development/extending-orion.md)
