"""Implementation of ``orion run``."""

from __future__ import annotations

import asyncio

from config import DEFAULT_USER_ID
from errors import OrionError


async def _read_line(prompt: str) -> str:
    """Read user input without blocking the event loop."""
    return (await asyncio.to_thread(input, prompt)).strip()


async def _ask(app, message: str, session) -> None:
    session.increment_messages()
    result = await app.runner.run_message(message=message, session=session)
    session.touch()

    if result["final_text"]:
        print(result["final_text"])
    else:
        print("(no final response text)")


async def _interactive() -> None:
    # Import lazily so ``version`` and parser help do not initialize agents.
    from runtime.app import OrionApp

    print("Orion (ADK). Type a question, or 'exit' to quit.\n")
    app = OrionApp(require_google_api_key=True)
    session = app.session_manager.start_conversation(
        user_id=DEFAULT_USER_ID,
        title="Orion Chat",
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
            except OrionError as exc:
                print(f"\n[{type(exc).__name__}] {exc}")
            print()
    finally:
        try:
            await app.close()
        except (asyncio.CancelledError, Exception):
            pass


async def _one_shot(message: str) -> None:
    from runtime.app import OrionApp

    app = OrionApp(require_google_api_key=True)
    session = app.session_manager.start_conversation(
        user_id=DEFAULT_USER_ID,
        title="Orion Chat",
    )
    try:
        await _ask(app, message, session)
    finally:
        try:
            await app.close()
        except (asyncio.CancelledError, Exception):
            pass


def run_orion(message: str | None = None) -> int:
    """Start Orion interactively, or process one supplied message."""
    if message:
        asyncio.run(_one_shot(message))
    else:
        asyncio.run(_interactive())
    return 0
