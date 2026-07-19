from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class DestructiveActionPolicy(BasePolicy):

    BLOCKED_TOOLS = {
        "delete_repository",
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:

        if request.tool_name not in self.BLOCKED_TOOLS:
            return None

        return GuardDecision(
            action=GuardAction.BLOCK,
            reason=f"The tool '{request.tool_name}' is blocked.",
            policy="destructive_action_policy",
        )
