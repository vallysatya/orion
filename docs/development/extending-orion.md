# Extending Orion

Orion v1.0 has **extension seams**, not a formal plugin system. You can compose
new behavior by implementing small interfaces and wiring them at construction
time.

## Guard policies

1. Subclass `policies.base_policy.BasePolicy`
2. Implement `evaluate(request) -> GuardDecision | None`
3. Insert the policy into the ordered list used by `build_guard_policies()` /
   `GuardService`

Return `None` when the policy does not apply. First non-`None` decision wins.

## Memory policies / storage

- Subclass `BaseMemoryPolicy` and add it to `MemoryPolicyEngine`
- Or implement `PersistentMemory` and inject it into `MemoryService` instead of
  `SQLiteMemory`

Remember: persistent keys are global unless you add namespacing.

## Observability

- Record events with `TraceService.record(...)`
- Record counters/timings with `MetricsService` helpers
- Implement `BaseExporter` and call `export(trace)` when you want output

Exporters are not automatically flushed today.

## Agents and tools

- Build additional Google ADK agents/tools
- Register `before_tool_callback` / `after_tool_callback` to keep Guard coverage
- Pass a custom root agent into `AgentRunner` if you bypass the default coordinator

## Session backends

Inject an ADK `BaseSessionService` into `ADKSessionAdapter` for non-default
session storage. Orion's own `SessionManager` remains an in-memory metadata
layer unless you replace that too.

## Configuration

Construct `OrionConfig` / section dataclasses directly, or use `ConfigLoader`
with a custom environ mapping (useful in tests).

## What is not a plugin API

There is no:

- plugin discovery / entry-point marketplace
- hot reload of policies
- stable public SDK versioning policy beyond package modules
- documented guarantee that top-level package names (`config`, `tools`, …) will
  remain forever collision-free

Treat extension as in-tree or carefully vendored composition until a plugin
framework lands (see [ROADMAP.md](../../ROADMAP.md)).

## Related docs

- [Architecture](../concepts/architecture.md)
- [Guard & approvals](../concepts/guard-and-approvals.md)
- [Memory model](../concepts/memory-model.md)
- [Testing](testing.md)
