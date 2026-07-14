"""Agent execution via Google ADK 2.4 public APIs."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types

from config import APP_NAME
from runtime.app import create_app
from runtime.session import get_or_create_session


def _user_content(message: str) -> types.Content:
    """Build a user Content message in the ADK / GenAI format."""
    return types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )


def _extract_text(event: Event) -> str:
    """Collect visible text from an ADK event."""
    if not event.content or not event.content.parts:
        return ""
    parts: list[str] = []
    for part in event.content.parts:
        text = getattr(part, "text", None)
        if text:
            parts.append(text)
    return "".join(parts)


class AgentRunner:
    """Wraps ADK App + InMemoryRunner lifecycle and message execution.

    Official local/dev path in ADK 2.4:
      App(name=..., root_agent=...)
      InMemoryRunner(app=app)
      await session_service.create_session(...)
      async for event in runner.run_async(..., new_message=Content(...))
    """

    def __init__(self) -> None:
        self._app = create_app()
        # Prefer App-based construction (recommended in ADK 2.x).
        self._runner = InMemoryRunner(app=self._app, app_name=APP_NAME)

    @property
    def runner(self) -> InMemoryRunner:
        return self._runner

    @property
    def app_name(self) -> str:
        return self._runner.app_name

    async def stream_message(
        self,
        message: str,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> AsyncIterator[Event]:
        """Stream ADK events for one user message."""
        session = await get_or_create_session(
            self._runner,
            user_id=user_id,
            session_id=session_id,
        )
        new_message = _user_content(message)

        async for event in self._runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=new_message,
        ):
            yield event

    async def run_message(
        self,
        message: str,
        *,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Run one message and return events + final text response."""
        events: list[Event] = []
        final_text = ""

        async for event in self.stream_message(
            message,
            user_id=user_id,
            session_id=session_id,
        ):
            events.append(event)
            text = _extract_text(event)
            if event.is_final_response() and text:
                final_text = text

        return {
            "events": events,
            "final_text": final_text,
        }

    async def close(self) -> None:
        await self._runner.close()
