# Configuration reference

Canonical environment variables for Orion v1.0.

Loaded by `ConfigLoader` in `src/config/loader.py`.

## Variables

| Variable | Default | Notes |
| --- | --- | --- |
| `GOOGLE_API_KEY` | unset | Required for `orion run` |
| `GITHUB_TOKEN` | unset | Required for authenticated/private GitHub ops |
| `GITHUB_API_BASE_URL` | `https://api.github.com` | Must start with `http://` or `https://` |
| `ORION_APP_NAME` | `orion` | Non-empty string |
| `ORION_DEFAULT_USER_ID` | `default-user` | Default Orion user id |
| `ORION_DEFAULT_SESSION_ID` | `default_session` | Compatibility default |
| `ORION_DEBUG` | `false` | Bool: `1/true/yes/on` or `0/false/no/off` |
| `ORION_MEMORY_DB` | `<project-root>/orion_memory.db` | Non-empty path when set |

## Typed structure

```text
OrionConfig
├── github: GitHubConfig(api_base_url, token)
├── runtime: RuntimeConfig(app_name, default_user_id, default_session_id, google_api_key, debug)
└── memory: MemoryConfig(database_path)
```

Public helpers:

- `get_settings() -> OrionConfig`
- `reload_settings(...)` (primarily for tests)
- `validate_configuration(...)`
- Compatibility constants: `GITHUB_TOKEN`, `APP_NAME`, `MEMORY_DATABASE_PATH`, …

## Dotenv locations

1. `<project-root>/.env`
2. `src/agents/github_agent/.env`
3. `src/github_agent/.env` (**override=True**, legacy)

Prefer the project-root `.env` only.

## Validation rules

`OrionConfig.validate(...)` enforces:

- non-empty `APP_NAME`
- HTTP(S) GitHub API base URL
- non-empty memory database path
- optional required Google API key / GitHub token flags

Secrets are never interpolated into error messages.

## CLI helpers

```bash
orion config show
orion config validate
orion config init
```

## Not configurable in v1.0 (hard-coded)

- Model name (`gemini-2.5-flash`)
- GitHub HTTP timeout (30s)
- Default guard / memory policy sets
- Trace/metrics exporter auto-flush behavior

## Related docs

- [Getting started: configuration](../getting-started/configuration.md)
- [Installation](../getting-started/installation.md)
