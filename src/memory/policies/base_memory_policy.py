from abc import ABC, abstractmethod
from typing import Any

from memory.memory_decision import MemoryDecision


class BaseMemoryPolicy(ABC):

    @abstractmethod
    def evaluate(
        self,
        key: str,
        value: Any,
    ) -> MemoryDecision | None:
        """
        Return a MemoryDecision if this policy applies,
        otherwise None.
        """
        pass
