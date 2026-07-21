# Configuration

Orion uses a typed configuration package (`src/config/`) loaded from the
process environment and optional `.env` files.

Canonical reference: [Configuration reference](../reference/configuration.md)

## Generate a template

```bash
orion config init                 # writes .env.example
orion config init --force         # overwrite existing template
orion config init --path my.env.example
```

Copy the template to `.env` and fill in values. Do not commit `.env`.

## Required vs optional secrets

| Variable | Required when |
| --- | --- |
| `GOOGLE_API_KEY` | Running agents (`orion run`) |
| `GITHUB_TOKEN` | Authenticated / private GitHub operations |

`orion config validate` checks structure and defaults. It does **not** require
secrets. `orion run` requires a Google API key. `orion doctor` reports whether
both secrets and repository memory look healthy.

## Inspect and validate

```bash
orion config show       # secrets appear as ******** or (not set)
orion config validate
```

Secret values never appear in:

- `OrionConfig` / config section `__repr__` output
- CLI `config show`
- typed configuration error messages
- GitHub integration error messages

## Dotenv load order

When configuration loads, Orion reads:

1. `<project-root>/.env`
2. `src/agents/github_agent/.env`
3. `src/github_agent/.env` (legacy path, loaded with **override**)

Prefer a single root `.env`. The legacy path can override earlier values —
including values that were already present in the process environment — because
it uses `override=True`.

## Common settings

```bash
# Runtime
GOOGLE_API_KEY=
ORION_APP_NAME=orion
ORION_DEFAULT_USER_ID=default-user
ORION_DEFAULT_SESSION_ID=default_session
ORION_DEBUG=false

# GitHub
GITHUB_TOKEN=
GITHUB_API_BASE_URL=https://api.github.com

# Memory
ORION_MEMORY_DB=                 # empty → <project-root>/orion_memory.db
```

Boolean values for `ORION_DEBUG`: `1/true/yes/on` or `0/false/no/off`
(case-insensitive). Invalid values raise `ConfigurationError`.

## Typed model

```text
OrionConfig
├── github: GitHubConfig
├── runtime: RuntimeConfig
└── memory: MemoryConfig
```

Loaded at import time via `ConfigLoader` and exposed as both
`get_settings()` and compatibility constants (`GITHUB_TOKEN`, `APP_NAME`, …).

## Next steps

- [Quickstart](quickstart.md)
- [Configuration reference](../reference/configuration.md)
