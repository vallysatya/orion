"""
Conversation state model for Orion.

This stores structured data associated with a conversation.
Unlike SessionInfo, this data changes frequently during
the lifetime of a conversation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationState:
    """
    Represents the current working state of a conversation.

    This model is intentionally generic so every Orion
    agent (GitHub, Gmail, Slack, Calendar, etc.) can use it.
    """

    # Generic key/value store
    context: dict[str, Any] = field(default_factory=dict)

    # Last tool executed
    last_tool: str | None = None

    # Last agent that handled the request
    last_agent: str | None = None

    # Optional active task
    current_task: str | None = None

    # -----------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------

    def set(self, key: str, value: Any) -> None:
        """Store a value in the conversation state."""
        self.context[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the conversation state."""
        return self.context.get(key, default)

    def remove(self, key: str) -> None:
        """Remove a value from the state."""
        self.context.pop(key, None)

    def clear(self) -> None:
        """Reset the conversation state."""
        self.context.clear()
        self.last_tool = None
        self.last_agent = None
        self.current_task = None
