from typing import Any, Sequence

from memory.memory_decision import MemoryDecision, MemoryStorage
from memory.policies.base_memory_policy import BaseMemoryPolicy


class MemoryPolicyEngine:
    """
    Evaluates memory policies in order and returns the first match.

    Default fallback is session-only storage.
    """

    def __init__(
        self,
        policies: Sequence[BaseMemoryPolicy],
    ) -> None:
        self._policies = policies

    def decide(
        self,
        key: str,
        value: Any = None,
    ) -> MemoryDecision:
        for policy in self._policies:
            decision = policy.evaluate(key, value)
            if decision is not None:
                return decision

        return MemoryDecision(
            storage=MemoryStorage.SESSION,
        )
