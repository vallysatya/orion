from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class ApprovalPolicy(BasePolicy):
    """Requires human approval for sensitive tool executions."""

    APPROVAL_REQUIRED_TOOLS = {
        "merge_pull_request",
        "create_repository",
        "update_repository_settings",
        "add_repository_collaborator",
        "remove_repository_collaborator",
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        if request.tool_name not in self.APPROVAL_REQUIRED_TOOLS:
            return None

        return GuardDecision(
            action=GuardAction.REQUIRE_APPROVAL,
            reason=(
                f"The tool '{request.tool_name}' requires human approval "
                "before execution."
            ),
            policy="approval_policy",
        )
