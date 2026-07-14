"""Orion CLI entry point — ask the GitHub agent interactively."""

from __future__ import annotations

import asyncio
import sys

from runtime.runner import AgentRunner


async def _ask(runner: AgentRunner, message: str) -> None:
    result = await runner.run_message(message)
    if result["final_text"]:
        print(result["final_text"])
    else:
        print("(no final response text)")


async def _read_line(prompt: str) -> str:
    """Read user input without blocking the event loop."""
    return (await asyncio.to_thread(input, prompt)).strip()


async def _interactive() -> None:
    print("Orion GitHub Agent (ADK). Type a question, or 'exit' to quit.\n")
    runner = AgentRunner()
    try:
        while True:
            try:
                message = await _read_line("You> ")
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                return

            if not message:
                continue
            if message.lower() in {"exit", "quit", "q"}:
                print("Bye.")
                return

            print("Orion> ", end="", flush=True)
            try:
                await _ask(runner, message)
            except asyncio.CancelledError:
                print("\nBye.")
                raise
            except Exception as exc:  # noqa: BLE001 - show CLI-friendly errors
                print(f"\nError: {exc}")
            print()
    finally:
        try:
            await runner.close()
        except (asyncio.CancelledError, Exception):
            pass


async def _one_shot(message: str) -> None:
    runner = AgentRunner()
    try:
        await _ask(runner, message)
    finally:
        try:
            await runner.close()
        except (asyncio.CancelledError, Exception):
            pass


def main() -> None:
    try:
        if len(sys.argv) > 1:
            asyncio.run(_one_shot(" ".join(sys.argv[1:])))
        else:
            asyncio.run(_interactive())
    except KeyboardInterrupt:
        # Ctrl+C during asyncio.run — exit quietly without a traceback.
        print("\nBye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
