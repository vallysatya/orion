# Contributing to Orion

Thanks for contributing. Orion aims to stay **honest**: every documented command
and feature should map to real implementation.

## Development setup

```bash
git clone https://github.com/vallysatya/orion.git
cd orion
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
orion version
pytest -q
```

See [docs/getting-started/installation.md](docs/getting-started/installation.md)
and [docs/development/testing.md](docs/development/testing.md).

## Project layout (mental model)

```text
src/
  cli/            Developer CLI
  config/         Typed configuration
  container/      Composition root
  runtime/        OrionApp + AgentRunner
  agents/         Coordinator + specialists
  policies/       Guard policies
  memory/         Dual memory
  observability/  Trace + metrics
  errors/         OrionError hierarchy
tests/            Pytest suite
docs/             Product documentation
```

## Coding guidelines

1. Prefer typed dataclasses and explicit error wrapping (`raise ... from exc`).
2. Never log, print, or embed secrets (tokens, API keys) in errors, traces, or tests.
3. Keep CLI commands truthful — do not add commands that cannot produce meaningful output.
4. Preserve existing public imports unless the PR intentionally migrates them.
5. Add or update tests with every behavior change.
6. Update docs when user-facing behavior changes (`docs/`, README, changelog).

## Tests and checks

```bash
pytest -q
python -m pyright
python -m build
```

Avoid relying on live GitHub calls in unit tests. Keep secrets out of fixtures.

## Pull requests

1. Branch from `main`
2. Keep PRs focused and reviewable
3. Include:
   - clear description of *why*
   - test plan / commands run
   - docs updates when needed
4. Do not commit `.env`, databases, or build artifacts

## Documentation

Docs live under `docs/` with source-of-truth rules described in
[docs/README.md](docs/README.md). Prefer precise language over marketing claims.

## Security issues

Do **not** open public issues for vulnerabilities. Follow [SECURITY.md](SECURITY.md).

## Community

Be respectful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Questions

Use GitHub Discussions or Issues for non-security questions — see [SUPPORT.md](SUPPORT.md).
