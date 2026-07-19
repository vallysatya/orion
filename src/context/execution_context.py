"""
Per-request execution context for Orion.

Carries identity for a single agent turn without mixing it into
long-lived SessionInfo or ConversationState.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class OrionExecutionContext:
    """
    Request-scoped context passed through one Orion execution.

    Unlike SessionInfo (conversation metadata) and ConversationState
    (working memory), this exists only for the current request.
    """

    request_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = "default-user"
    session_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
