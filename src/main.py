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


async def _interactive() -> None:
    print("Orion GitHub Agent (ADK). Type a question, or 'exit' to quit.\n")
    runner = AgentRunner()
    try:
        while True:
            try:
                message = input("You> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break

            if not message:
                continue
            if message.lower() in {"exit", "quit", "q"}:
                print("Bye.")
                break

            print("Orion> ", end="", flush=True)
            try:
                await _ask(runner, message)
            except Exception as exc:  # noqa: BLE001 - show CLI-friendly errors
                print(f"\nError: {exc}")
            print()
    finally:
        await runner.close()


async def _one_shot(message: str) -> None:
    runner = AgentRunner()
    try:
        await _ask(runner, message)
    finally:
        await runner.close()


def main() -> None:
    if len(sys.argv) > 1:
        asyncio.run(_one_shot(" ".join(sys.argv[1:])))
    else:
        asyncio.run(_interactive())


if __name__ == "__main__":
    main()
