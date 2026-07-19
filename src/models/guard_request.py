from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GuardRequest:
    """Information required to evaluate a requested tool execution."""

    request_id: str
    user_id: str
    session_id: str
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    agent_name: str | None = None
    environment: str = "development"
