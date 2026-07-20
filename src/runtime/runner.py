"""Agent execution via Google ADK 2.4 public APIs."""

from __future__ import annotations

import time
from collections.abc import AsyncIterator
from typing import Any

from google.adk.agents import BaseAgent
from google.adk.apps import App
from google.adk.artifacts import InMemoryArtifactService
from google.adk.events import Event
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.genai import types

from config import APP_NAME
from models.session_info import SessionInfo
from observability.metrics.metrics_service import MetricsService
from observability.trace_service import TraceService
from runtime.adk_session_adapter import ADKSessionAdapter


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
    """
    Executes agent turns via ADK.

    Owns ADK App + Runner only.
    Does not own Orion conversation metadata (titles, favorites, etc.).
    Uses ADKSessionAdapter to map SessionInfo → ADK SessionService.
    """

    def __init__(
        self,
        agent: BaseAgent,
        *,
        session_adapter: ADKSessionAdapter,
        trace_service: TraceService,
        metrics_service: MetricsService,
    ) -> None:
        self._adk_app = App(name=APP_NAME, root_agent=agent)
        self._session_adapter = session_adapter
        self._trace_service = trace_service
        self._metrics_service = metrics_service
        # Share the adapter's SessionService so create/get stay in sync.
        self._runner = Runner(
            app=self._adk_app,
            app_name=APP_NAME,
            session_service=session_adapter.service,
            artifact_service=InMemoryArtifactService(),
            memory_service=InMemoryMemoryService(),
        )

    @property
    def runner(self) -> Runner:
        return self._runner

    @property
    def app_name(self) -> str:
        return self._runner.app_name

    async def stream_message(
        self,
        message: str,
        *,
        session: SessionInfo,
    ) -> AsyncIterator[Event]:
        """Stream ADK events for one user message."""
        self._trace_service.record(
            component="OrionRuntime",
            event="RequestStarted",
            metadata={
                "session_id": session.session_id,
                "user_id": session.user_id,
                "message_length": len(message),
            },
        )

        try:
            adk_session = await self._session_adapter.ensure_session(session)
            new_message = _user_content(message)

            async for event in self._runner.run_async(
                user_id=adk_session.user_id,
                session_id=adk_session.id,
                new_message=new_message,
            ):
                yield event
        except Exception as exc:
            self._trace_service.record(
                component="OrionRuntime",
                event="RequestFailed",
                metadata={
                    "session_id": session.session_id,
                    "error_type": type(exc).__name__,
                },
            )
            raise

    async def run_message(
        self,
        message: str,
        *,
        session: SessionInfo,
    ) -> dict[str, Any]:
        """Run one message and return events + final text response."""
        events: list[Event] = []
        final_text = ""
        started = time.perf_counter()
        self._metrics_service.record_request_started()

        try:
            async for event in self.stream_message(message, session=session):
                events.append(event)
                text = _extract_text(event)
                if event.is_final_response() and text:
                    final_text = text

            duration_ms = (time.perf_counter() - started) * 1000
            self._metrics_service.record_request_succeeded(duration_ms)
            self._trace_service.record(
                component="OrionRuntime",
                event="RequestCompleted",
                metadata={
                    "session_id": session.session_id,
                    "event_count": len(events),
                    "has_final_text": bool(final_text),
                },
            )
        except Exception:
            duration_ms = (time.perf_counter() - started) * 1000
            self._metrics_service.record_request_failed(duration_ms)
            raise

        return {
            "events": events,
            "final_text": final_text,
        }

    async def close(self) -> None:
        await self._runner.close()
