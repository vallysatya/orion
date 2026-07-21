# GitHub assistant guide

Orion's GitHub agent answers repository questions through **read-only** tools
backed by the GitHub REST API.

## What you can ask

Examples that work well:

```text
list my repositories
show open issues for owner/repo
summarize pull requests in owner/repo
who contributed to owner/repo recently?
what languages does owner/repo use?
what is the license for owner/repo?
```

```bash
orion run "list open issues for vallysatya/orion"
```

## Supported operations (v1.0)

The GitHub client and tools currently support:

- Repository information and search
- Authenticated repository listing (`list my repositories`)
- Open issues and pull requests
- Latest release
- Contributors and commits
- Languages, topics, and license

There are **no** create / update / merge / delete GitHub tools in v1.0.

Policies such as `destructive_action_policy` and `approval_policy` still exist
for future mutating tools and for any custom tools you register. They are not
reachable through the built-in GitHub surface today.

## Authentication

| Scenario | Token needed? |
| --- | --- |
| Public repository reads | Usually no |
| Private repositories | Yes — `GITHUB_TOKEN` |
| `list my repositories` | Yes — `GITHUB_TOKEN` |

Set the token in `.env`:

```bash
GITHUB_TOKEN=ghp_...
GITHUB_API_BASE_URL=https://api.github.com
```

## Repository memory

The assistant can remember a current repository in **session** memory
(`current_repository`). Preferences such as `default_repository` can be stored
in both session and SQLite (dual memory).

Session memory is lost when the process exits. Persistent keys survive in
`orion_memory.db` (or `ORION_MEMORY_DB`).

## Guard interaction

Every GitHub tool call still passes through `before_tool_callback` →
`GuardService`. That means:

- Prompt-injection language in tool arguments can be blocked
- PII-looking argument content can be blocked
- Allowed calls still record metrics and traces

The LLM security-review agent (when used) is **advisory**. The callback Guard
is authoritative.

## Errors

GitHub failures surface as `GitHubIntegrationError` with structured fields such
as `operation`, `method`, `endpoint`, and `status_code`. Authorization headers
and response bodies are not included.

```text
[GitHubIntegrationError] ...
```

## Tips

1. Prefer explicit `owner/repo` in prompts when no repository is remembered.
2. Run `orion doctor` if authenticated calls fail — it checks token presence.
3. Use `orion memory stats` to confirm the SQLite path after remembering prefs.

## Related docs

- [Security guard guide](security-guard.md)
- [Memory management](memory-management.md)
- [Architecture](../concepts/architecture.md)
- [Errors reference](../reference/errors.md)
