from typing import Any

from memory.memory_decision import (
    MemoryDecision,
    MemoryStorage,
)
from memory.policies.base_memory_policy import BaseMemoryPolicy


PERSISTENT_KEYS = {
    "user_name",
    "preferred_language",
    "explanation_style",
}


class PersistencePolicy(BaseMemoryPolicy):

    def evaluate(
        self,
        key: str,
        value: Any,
    ) -> MemoryDecision | None:
        if key in PERSISTENT_KEYS:
            return MemoryDecision(
                storage=MemoryStorage.PERSISTENT,
            )

        return None
