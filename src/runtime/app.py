"""
Application bootstrap for Orion.
"""

from __future__ import annotations

from agents.coordinator_agent import coordinator_agent
from runtime.adk_session_adapter import ADKSessionAdapter
from runtime.runner import AgentRunner
from sessions.session_manager import SessionManager


class OrionApp:
    """
    Orion Application.

    Owns long-lived application services via dependency injection
    (no global singletons).
    """

    def __init__(self) -> None:
        self.session_manager = SessionManager()
        # Adapter shares one ADK SessionService with AgentRunner.
        self.adk_sessions = ADKSessionAdapter()
        self.runner = AgentRunner(
            agent=coordinator_agent,
            session_adapter=self.adk_sessions,
        )

    async def close(self) -> None:
        """Release runtime resources."""
        await self.runner.close()
