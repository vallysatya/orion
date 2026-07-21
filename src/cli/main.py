"""Console entry point for Orion."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from cli.config_command import run_config
from cli.doctor_command import run_doctor
from cli.guard_command import run_guard
from cli.memory_command import run_memory
from cli.output import configure_stdout
from cli.run_command import run_orion
from cli.version_command import run_version
from errors import OrionError


def build_parser() -> argparse.ArgumentParser:
    """Build the Orion command parser."""
    parser = argparse.ArgumentParser(
        prog="orion",
        description="Orion multi-agent platform",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Start Orion")
    run_parser.add_argument(
        "message",
        nargs="*",
        help="Optional one-shot message",
    )

    subparsers.add_parser(
        "doctor",
        help="Check configuration and dependencies",
    )
    subparsers.add_parser("version", help="Print Orion version")
    subparsers.add_parser("help", help="Show all commands")

    config_parser = subparsers.add_parser(
        "config",
        help="Inspect and manage configuration",
    )
    config_sub = config_parser.add_subparsers(
        dest="config_action",
        required=True,
    )
    config_sub.add_parser(
        "show",
        help="Display current configuration (secrets redacted)",
    )
    config_sub.add_parser("validate", help="Validate configuration")
    init_parser = config_sub.add_parser(
        "init",
        help="Generate a sample .env template",
    )
    init_parser.add_argument(
        "--path",
        default=".env.example",
        help="Where to write the template (default: .env.example)",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing file",
    )

    guard_parser = subparsers.add_parser(
        "guard",
        help="Inspect and test the security guard",
    )
    guard_sub = guard_parser.add_subparsers(
        dest="guard_action",
        required=True,
    )
    guard_sub.add_parser("status", help="Show loaded guard policies")
    guard_sub.add_parser(
        "test",
        help="Run sample tool calls through the guard",
    )

    memory_parser = subparsers.add_parser(
        "memory",
        help="Inspect and manage persistent memory",
    )
    memory_sub = memory_parser.add_subparsers(
        dest="memory_action",
        required=True,
    )
    memory_sub.add_parser("stats", help="Show memory statistics")
    clear_parser = memory_sub.add_parser("clear", help="Clear the database")
    clear_parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm clearing all memory entries",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch an Orion CLI command."""
    configure_stdout()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            message = " ".join(args.message).strip() or None
            return run_orion(message)
        if args.command == "doctor":
            return run_doctor()
        if args.command == "version":
            return run_version()
        if args.command == "help":
            parser.print_help()
            return 0
        if args.command == "config":
            from pathlib import Path

            return run_config(
                args.config_action,
                target=Path(getattr(args, "path", ".env.example")),
                force=getattr(args, "force", False),
            )
        if args.command == "guard":
            return run_guard(args.guard_action)
        if args.command == "memory":
            return run_memory(
                args.memory_action,
                confirm=getattr(args, "yes", False),
            )
    except KeyboardInterrupt:
        print("\nBye.")
        return 130
    except OrionError as exc:
        print(f"[{type(exc).__name__}] {exc}")
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
