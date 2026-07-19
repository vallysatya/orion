"""
Session metadata model for Orion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from models.conversation_state import ConversationState


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class SessionInfo:
    """
    Represents a conversation inside Orion.

    SessionInfo = who/what is this conversation? (metadata)
    ConversationState = what does Orion currently know? (working data)

    This class does NOT store ADK session objects.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = "default-user"

    title: str = "New Conversation"

    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    active: bool = False
    message_count: int = 0

    state: ConversationState = field(default_factory=ConversationState)

    def touch(self) -> None:
        """Update the last activity timestamp."""
        self.updated_at = _utc_now()

    def increment_messages(self) -> None:
        """Increment the total message count."""
        self.message_count += 1
        self.touch()
