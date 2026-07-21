"""Backward-compatible module entry point for the Orion CLI."""

from cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())
