# Testing

## Setup

```bash
pip install -e ".[dev]"
pytest -q
```

Editable install is preferred so imports resolve without manual `PYTHONPATH`.

If you only installed requirements:

```powershell
$env:PYTHONPATH = "src"
pytest -q
```

## What the suite covers

Roughly **116** tests across:

- CLI commands
- Typed configuration / secret redaction
- Error hierarchy
- Guard evaluation and tracing
- Memory policies / SQLite / metrics
- Runtime tracing and error wrapping
- GitHub client tracing, metrics, and error mapping
- Tool callback allow/block/approval paths
- Container wiring for trace and metrics

## Type checking

```bash
python -m pyright
```

Pyright is configured via `pyproject.toml` / `pyrightconfig.json` with
`extraPaths = ["src"]`.

## Packaging checks

```bash
python -m build
orion version
```

Confirm `dist/` artifacts exclude tests, `.env*`, and `*.db`.

## Scripts (manual)

Under `scripts/`:

| Script | Notes |
| --- | --- |
| `scripts/test_guard_service.py` | Local deterministic Guard demo |
| `scripts/test_github_tools.py` | **Live** GitHub API calls |
| `scripts/check_env.py` | Prints presence/length of secrets (not values) |

Do not treat live GitHub scripts as CI-safe by default.

## Caveats

1. Some older `tests/test_*.py` files contain top-level demo code that runs during
   collection and may create/touch `orion_memory.db`.
2. Prefer isolating experiments with `ORION_MEMORY_DB` pointing at a temp path.
3. Never commit `.env` files or paste tokens into test output.
4. Dependencies are unpinned — ADK upgrades can change behavior.

## Related docs

- [Release process](release-process.md)
- [Contributing](../../CONTRIBUTING.md)
