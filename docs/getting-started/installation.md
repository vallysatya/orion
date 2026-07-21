# Installation

Orion targets **Python 3.11+** and installs as a normal setuptools package with a
`src/` layout.

## Prerequisites

- Python 3.11 or newer
- `pip` and `venv`
- A Google AI / Gemini API key for agent runs
- (Optional) A GitHub personal access token for authenticated GitHub operations

## Create a virtual environment

```bash
cd orion
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

## Install Orion

### Recommended (developers)

Installs Orion in editable mode **and** development tools (`pytest`, `build`, `pyright`):

```bash
pip install -e ".[dev]"
```

### Runtime only

Installs Orion and its runtime dependencies, and registers the `orion` console script:

```bash
pip install .
```

### Dependencies only (not recommended)

```bash
pip install -r requirements.txt
```

This installs `python-dotenv`, `httpx`, and `google-adk` **only**. It does **not**:

- install the Orion package
- register the `orion` console command
- include development extras

If you use this path for local hacking, you must set `PYTHONPATH=src` yourself.

## Verify the install

```bash
orion version
# Orion 1.0.1

orion help
```

## Build distributions (optional)

```bash
pip install -e ".[dev]"   # ensures `build` is available
python -m build
```

Artifacts appear under `dist/`:

- `orion-1.0.1-py3-none-any.whl`
- `orion-1.0.1.tar.gz`

Package discovery includes Orion modules under `src/` and excludes tests, `.env`
files, databases, caches, and build artifacts. See `MANIFEST.in` and
`pyproject.toml`.

## Console entry point

The installed command is defined as:

```toml
[project.scripts]
orion = "cli.main:main"
```

That maps to `src/cli/main.py:main`. There is no `python -m orion` entry point
in v1.0.

## Next steps

1. [Configure Orion](configuration.md)
2. [Run the quickstart](quickstart.md)
