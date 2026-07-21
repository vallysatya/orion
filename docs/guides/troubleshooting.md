# Troubleshooting

Common Orion failures and how to resolve them.

## `orion` is not recognized

**Cause:** Orion was not installed as a package (for example only
`pip install -r requirements.txt`).

**Fix:**

```bash
pip install -e ".[dev]"
# or
pip install .
orion version
```

## `ConfigurationError: GOOGLE_API_KEY is required`

**Cause:** Running agents without a Google API key.

**Fix:** Put `GOOGLE_API_KEY=...` in `.env` (project root), then:

```bash
orion config show
orion doctor
```

## GitHub calls fail with `GitHubIntegrationError`

Checklist:

1. Is `GITHUB_TOKEN` set for private / authenticated operations?
2. Is `GITHUB_API_BASE_URL` an `http://` or `https://` URL?
3. Does the token have the scopes you need?
4. Is the repository name correct (`owner/repo`)?

Inspect without leaking secrets:

```bash
orion config show
orion doctor
```

## `orion doctor` reports missing repository

Doctor looks for `default_repository` or `current_repository` in persistent
memory. A missing value is not fatal for all tasks — set a repository during
conversation or ensure preferences were saved.

## Guard blocks unexpected tool calls

Prompt-injection / PII policies scan **tool arguments** with regexes. Clean up
argument text or adjust custom policies if you maintain your own stack.

Verify baseline behavior:

```bash
orion guard test
```

## Memory database surprises

Symptoms:

- Unexpected `orion_memory.db` appears after `doctor`, `memory stats`, or tests
- Preferences shared across what you thought were separate users

Notes:

- Opening SQLite creates the DB if missing
- Persistent keys are global (not per-user)
- Some demo test modules under `tests/` may touch the default DB during
  collection — prefer an isolated `ORION_MEMORY_DB` when experimenting

## Import-time configuration errors

Invalid `ORION_DEBUG` (or similar) can fail during config import, before the CLI
`OrionError` handler runs, producing a traceback. Fix the env value and retry.

## Windows console encoding issues

Orion tries to use UTF-8 for status marks (`✓`, `✔`). If your console cannot
encode them, it falls back to ASCII (`OK`, `PASS`, `X`). This is expected.

## `python -m build` fails with `No module named build`

```bash
pip install -e ".[dev]"
# or
pip install build
python -m build
```

## Tests fail with import errors

Prefer editable install so packages resolve without manual `PYTHONPATH`:

```bash
pip install -e ".[dev]"
pytest -q
```

## Still stuck?

1. Collect `orion version`, `orion doctor`, and the typed error name
2. Search existing GitHub Issues
3. Open a new issue with reproduction steps (never paste secrets)

See [SUPPORT.md](../../SUPPORT.md).
