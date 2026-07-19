from abc import ABC, abstractmethod

from models.guard_decision import GuardDecision
from models.guard_request import GuardRequest


class BasePolicy(ABC):
    """
    Base class for every Orion security policy.
    """

    @abstractmethod
    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        """
        Evaluate a GuardRequest.

        Returns:
            GuardDecision if this policy applies.
            None if this policy is not applicable.
        """
        pass
