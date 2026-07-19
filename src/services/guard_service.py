from collections.abc import Sequence

from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class GuardService:
    """Coordinates Orion security policies."""

    def __init__(self, policies: Sequence[BasePolicy]):
        self._policies = list(policies)

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision:

        for policy in self._policies:
            decision = policy.evaluate(request)

            if decision is not None:
                return decision

        return GuardDecision(
            action=GuardAction.ALLOW,
            reason="Tool execution allowed.",
            policy="default_policy",
        )
