from typing import Any

from memory.memory_decision import (
    MemoryDecision,
    MemoryStorage,
)
from memory.policies.base_memory_policy import BaseMemoryPolicy


SESSION_KEYS = {
    "current_repository",
    "environment",
    "risk_score",
    "approval_required",
    "last_tool",
    "last_security_decision",
}


class SessionPolicy(BaseMemoryPolicy):

    def evaluate(
        self,
        key: str,
        value: Any,
    ) -> MemoryDecision | None:
        if key in SESSION_KEYS:
            return MemoryDecision(
                storage=MemoryStorage.SESSION,
            )

        return None
