from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class EnvironmentPolicy(BasePolicy):
    """Applies stricter controls in production environments."""

    PRODUCTION_ENVIRONMENTS = {
        "production",
        "prod",
    }

    PRODUCTION_BLOCKED_TOOLS = {
        "delete_repository",
        "delete_branch",
        "disable_repository_security",
    }

    PRODUCTION_APPROVAL_TOOLS = {
        "merge_pull_request",
        "update_repository_settings",
        "remove_repository_collaborator",
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        environment = getattr(request, "environment", None)

        if environment is None:
            return None

        normalized_environment = str(environment).lower()

        if normalized_environment not in self.PRODUCTION_ENVIRONMENTS:
            return None

        if request.tool_name in self.PRODUCTION_BLOCKED_TOOLS:
            return GuardDecision(
                action=GuardAction.BLOCK,
                reason=(
                    f"The tool '{request.tool_name}' is blocked in the "
                    f"'{normalized_environment}' environment."
                ),
                policy="environment_policy",
            )

        if request.tool_name in self.PRODUCTION_APPROVAL_TOOLS:
            return GuardDecision(
                action=GuardAction.REQUIRE_APPROVAL,
                reason=(
                    f"The tool '{request.tool_name}' requires approval in the "
                    f"'{normalized_environment}' environment."
                ),
                policy="environment_policy",
            )

        return None
