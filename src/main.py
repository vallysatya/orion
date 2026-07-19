"""Orion CLI entry point — application orchestrator."""

from __future__ import annotations

import asyncio
import sys

from runtime.app import OrionApp


async def _read_line(prompt: str) -> str:
    """Read user input without blocking the event loop."""
    return (await asyncio.to_thread(input, prompt)).strip()


async def _ask(app: OrionApp, message: str, session) -> None:
    session.increment_messages()

    result = await app.runner.run_message(
        message=message,
        session=session,
    )

    session.touch()

    if result["final_text"]:
        print(result["final_text"])
    else:
        print("(no final response text)")


async def _interactive() -> None:
    print("Orion GitHub Agent (ADK). Type a question, or 'exit' to quit.\n")

    app = OrionApp()
    session = app.session_manager.start_conversation(
        user_id="default-user",
        title="GitHub Chat",
    )
    print(f"Session: {session.title} ({session.session_id[:8]}…)\n")

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
                await _ask(app, message, session)
            except asyncio.CancelledError:
                print("\nBye.")
                raise
            except Exception as exc:  # noqa: BLE001 - show CLI-friendly errors
                print(f"\nError: {exc}")
            print()
    finally:
        try:
            await app.close()
        except (asyncio.CancelledError, Exception):
            pass


async def _one_shot(message: str) -> None:
    app = OrionApp()
    session = app.session_manager.start_conversation(
        user_id="default-user",
        title="GitHub Chat",
    )
    try:
        await _ask(app, message, session)
    finally:
        try:
            await app.close()
        except (asyncio.CancelledError, Exception):
            pass


def main() -> None:
    try:
        if len(sys.argv) > 1:
            asyncio.run(_one_shot(" ".join(sys.argv[1:])))
        else:
            asyncio.run(_interactive())
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
