"""
ADK session adapter.

Bridges Orion's SessionInfo model with Google ADK's SessionService.
ADK provides the service (e.g. InMemorySessionService); this class adapts
Orion conversation metadata onto that API.
"""

from __future__ import annotations

from google.adk.sessions import InMemorySessionService
from google.adk.sessions.base_session_service import BaseSessionService
from google.adk.sessions.session import Session

from config import APP_NAME
from models.session_info import SessionInfo


class ADKSessionAdapter:
    """
    Adapter between Orion SessionInfo and ADK sessions.

    Orion owns SessionInfo (titles, activity, etc.).
    ADK owns Session objects via SessionService.

    This class is not a domain service — it adapts one model to ADK's API.
    """

    def __init__(
        self,
        session_service: BaseSessionService | None = None,
    ) -> None:
        # Prefer an injected service so this shares state with AgentRunner.
        self._session_service = session_service or InMemorySessionService()

    @property
    def service(self) -> BaseSessionService:
        """Return the underlying ADK SessionService."""
        return self._session_service

    async def create_adk_session(self, session: SessionInfo) -> Session:
        """Create an ADK session from Orion SessionInfo."""
        return await self._session_service.create_session(
            app_name=APP_NAME,
            user_id=session.user_id,
            session_id=session.session_id,
        )

    async def get_adk_session(self, session: SessionInfo) -> Session | None:
        """Retrieve the ADK session for an Orion SessionInfo."""
        return await self._session_service.get_session(
            app_name=APP_NAME,
            user_id=session.user_id,
            session_id=session.session_id,
        )

    async def ensure_session(self, session: SessionInfo) -> Session:
        """Return an existing ADK session or create one for SessionInfo."""
        existing = await self.get_adk_session(session)
        if existing is not None:
            return existing
        return await self.create_adk_session(session)

    async def delete_adk_session(self, session: SessionInfo) -> None:
        """Delete the ADK session that corresponds to SessionInfo."""
        await self._session_service.delete_session(
            app_name=APP_NAME,
            user_id=session.user_id,
            session_id=session.session_id,
        )
