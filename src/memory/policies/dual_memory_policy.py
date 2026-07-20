from typing import Any

from memory.memory_decision import (
    MemoryDecision,
    MemoryStorage,
)
from memory.policies.base_memory_policy import BaseMemoryPolicy


BOTH_KEYS = {
    "default_repository",
}


class DualMemoryPolicy(BaseMemoryPolicy):
    """
    Keys that should be available immediately in session state
    and also survive restarts via persistent storage.
    """

    def evaluate(
        self,
        key: str,
        value: Any,
    ) -> MemoryDecision | None:
        if key in BOTH_KEYS:
            return MemoryDecision(
                storage=MemoryStorage.BOTH,
            )

        return None
