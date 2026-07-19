"""
Session Manager for Orion.

Responsible for creating and managing conversations.
This class is independent of Google ADK.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from models.session_info import SessionInfo


class SessionManager:
    """
    Manages Orion conversations.

    Owns conversation metadata (titles, activity, switching).
    Does not own ADK execution — that belongs to AgentRunner.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionInfo] = {}
        self._active_session_id: Optional[str] = None

    # --------------------------------------------------------
    # Conversation lifecycle
    # --------------------------------------------------------

    def start_conversation(
        self,
        user_id: str = "default-user",
        title: str = "New Conversation",
        *,
        resume_active: bool = False,
    ) -> SessionInfo:
        """
        Start a conversation for the caller.

        Today this creates a new session (or resumes the active one when
        resume_active=True). Later it can choose create / resume / restore
        from persistence without changing main.py.
        """
        if resume_active:
            active = self.get_active_session()
            if active is not None:
                return active

        return self.create_session(user_id=user_id, title=title)

    def create_session(
        self,
        user_id: str = "default-user",
        title: str = "New Conversation",
    ) -> SessionInfo:
        """Create a new conversation and make it active."""
        session = SessionInfo(
            user_id=user_id,
            title=title,
            active=True,
        )

        if self._active_session_id and self._active_session_id in self._sessions:
            self._sessions[self._active_session_id].active = False

        self._sessions[session.session_id] = session
        self._active_session_id = session.session_id
        return session

    # --------------------------------------------------------
    # Session Lookup
    # --------------------------------------------------------

    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Return a session by its ID."""
        return self._sessions.get(session_id)

    def list_sessions(self) -> List[SessionInfo]:
        """Return all sessions."""
        return list(self._sessions.values())

    def get_active_session(self) -> Optional[SessionInfo]:
        """Return the currently active session."""
        if not self._active_session_id:
            return None
        return self._sessions.get(self._active_session_id)

    # --------------------------------------------------------
    # Session Switching
    # --------------------------------------------------------

    def switch_session(self, session_id: str) -> bool:
        """Make another session active."""
        if session_id not in self._sessions:
            return False

        if self._active_session_id and self._active_session_id in self._sessions:
            self._sessions[self._active_session_id].active = False

        self._sessions[session_id].active = True
        self._active_session_id = session_id
        return True

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    def delete_session(self, session_id: str) -> bool:
        """Delete a conversation."""
        if session_id not in self._sessions:
            return False

        del self._sessions[session_id]

        if self._active_session_id == session_id:
            self._active_session_id = None

        return True
