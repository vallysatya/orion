# CLI reference

Console entry point: `orion = cli.main:main` → `src/cli/main.py`.

```text
orion [-h] {run,doctor,version,help,config,guard,memory} ...
```

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | Failed check/test/validation, refused destructive action, or caught `OrionError` |
| `2` | Argparse / unknown action |
| `130` | KeyboardInterrupt at top-level handler |

## `orion run`

Start an interactive session or process one message.

```bash
orion run
orion run list my repositories
orion run "list my repositories"
```

| Behavior | Detail |
| --- | --- |
| Requires | `GOOGLE_API_KEY` |
| Interactive exits | `exit`, `quit`, `q` |
| Empty final text | prints `(no final response text)` |
| Message-level errors | typed Orion errors printed; session continues |

## `orion doctor`

Health checks:

1. GitHub token configured
2. Repository configured (from persistent memory)
3. Memory database available
4. Model/API configuration valid (`GOOGLE_API_KEY`)

Returns `0` if all pass, else `1`.

Side effect: importing shared services may create the SQLite database if missing.
Doctor does **not** call the live GitHub API.

## `orion version`

```bash
orion version
# Orion 1.0.1
```

## `orion help`

Prints the same top-level help as `orion --help` / `orion -h`.

## `orion config`

### `show`

Prints current settings with secrets redacted (`********` / `(not set)`).

### `validate`

Validates structure/defaults. Does not require secrets. Exit `0`/`1`.

### `init`

```bash
orion config init
orion config init --path .env.example
orion config init --force
```

Writes a template. Refuses overwrite without `--force`.

## `orion guard`

### `status`

Lists loaded policy class names in evaluation order.

### `test`

Runs four deterministic scenarios (safe / PII / injection / approval). Exit
`0` if all match expected decisions.

## `orion memory`

### `stats`

Shows database path, entry count, and file size. Opening the DB may create it.

### `clear`

```bash
orion memory clear --yes
```

Without `--yes`, refuses and exits `1`. Clears **all** persistent entries.

## Intentionally not shipped

These commands are deferred until durable / out-of-process surfaces exist:

- `orion metrics`
- `orion trace`
- `orion session`
- `orion agent`
- `orion plugin`
- `orion serve`

## Related docs

- [Quickstart](../getting-started/quickstart.md)
- [Troubleshooting](../guides/troubleshooting.md)
