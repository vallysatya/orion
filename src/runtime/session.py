"""Session helpers for ADK runtime (ADK 2.4)."""

from __future__ import annotations

from google.adk.runners import Runner
from google.adk.sessions import Session

from config import DEFAULT_SESSION_ID, DEFAULT_USER_ID


def resolve_session_ids(
    user_id: str | None = None,
    session_id: str | None = None,
) -> tuple[str, str]:
    """Return the user and session IDs to use for a run."""
    return user_id or DEFAULT_USER_ID, session_id or DEFAULT_SESSION_ID


async def get_or_create_session(
    runner: Runner,
    *,
    user_id: str | None = None,
    session_id: str | None = None,
) -> Session:
    """Fetch an existing ADK session or create one.

    ADK 2.4 session APIs are async. create_session must be awaited, and the
    session must live on the same session_service instance as the runner.
    """
    resolved_user_id, resolved_session_id = resolve_session_ids(
        user_id=user_id,
        session_id=session_id,
    )

    session = await runner.session_service.get_session(
        app_name=runner.app_name,
        user_id=resolved_user_id,
        session_id=resolved_session_id,
    )
    if session is not None:
        return session

    return await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=resolved_user_id,
        session_id=resolved_session_id,
    )
