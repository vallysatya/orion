# Release process

Orion uses setuptools packaging with a `src/` layout.

## Version sources

Keep these aligned on release:

| Location | Field |
| --- | --- |
| `pyproject.toml` | `project.version` |
| `src/orion/__init__.py` | `__version__` |
| `CHANGELOG.md` | release section |
| Git tag | `vX.Y.Z` |

## Pre-release checklist

1. Update `CHANGELOG.md` (move Unreleased notes into a dated section)
2. Bump version strings
3. Confirm docs match shipped CLI/behavior (no placeholder commands)
4. Run verification:

```bash
pip install -e ".[dev]"
pytest -q
orion version
orion help
orion guard test
python -m build
```

5. Inspect artifacts:

```bash
# wheel / sdist should exclude tests, .env, databases
```

6. Commit, tag, push:

```bash
git tag -a v1.0.0 -m "Orion v1.0.0"
git push origin main --tags
```

## Artifact expectations

`python -m build` produces:

- `dist/orion-<version>-py3-none-any.whl`
- `dist/orion-<version>.tar.gz`

Entry point inside metadata:

```text
orion = cli.main:main
```

Runtime dependencies: `python-dotenv`, `httpx`, `google-adk`  
Dev extras: `build`, `pytest`, `pyright`

## What not to publish

- `.env` / secrets
- local SQLite databases
- `build/`, `dist/` (regenerate; typically gitignored)
- personal journals / local-only docs

## Post-release

- Update `ROADMAP.md` if priorities changed
- Open GitHub Release notes from the changelog section
- Watch Issues for install/entry-point regressions

## Related docs

- [Testing](testing.md)
- [Changelog](../../CHANGELOG.md)
- [Roadmap](../../ROADMAP.md)
