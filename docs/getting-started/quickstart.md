# Quickstart

Get from zero to a working Orion session in a few minutes.

## 1. Install

```bash
pip install -e ".[dev]"
orion version
```

See [Installation](installation.md) for platform-specific details.

## 2. Create configuration

```bash
orion config init
```

This writes `.env.example`. Copy it to `.env` and edit:

```powershell
# Windows
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Minimum contents:

```bash
GOOGLE_API_KEY=your-google-api-key
GITHUB_TOKEN=your-github-token
```

Notes:

- `GOOGLE_API_KEY` is **required** for `orion run`
- `GITHUB_TOKEN` is **optional** for public repositories, **required** for private repos and authenticated listing (for example `list my repositories`)

Never commit `.env`. Orion's `.gitignore` already excludes `.env` and `.env.*`.

## 3. Check your environment

```bash
orion doctor
orion config show
orion config validate
```

`config show` always redacts secrets (`********`).

## 4. Exercise Guard (optional but recommended)

```bash
orion guard status
orion guard test
```

Expected `guard test` scenarios:

```text
✔ Safe Tool Call
✔ PII Detection
✔ Prompt Injection Detection
✔ Approval Flow
```

## 5. Run Orion

One-shot:

```bash
orion run "summarize this repository's purpose"
```

Interactive:

```bash
orion run
```

```text
Orion (ADK). Type a question, or 'exit' to quit.

Session: Orion Chat (abcd1234…)

You> list open issues for my default repository
Orion> ...
You> exit
```

Exit with `exit`, `quit`, or `q`.

## 6. Inspect memory

```bash
orion memory stats
```

Clear persistent memory only when you intend to wipe preferences:

```bash
orion memory clear --yes
```

## What good looks like

| Check | Expected |
| --- | --- |
| `orion version` | `Orion 1.0.1` |
| `orion doctor` | green checks (or clear next steps) |
| `orion guard test` | four scenarios pass |
| `orion run "..."` | final agent text (or a typed Orion error) |

## Next reading

- [Configuration](configuration.md)
- [GitHub assistant guide](../guides/github-assistant.md)
- [Architecture](../concepts/architecture.md)
- [Troubleshooting](../guides/troubleshooting.md)
