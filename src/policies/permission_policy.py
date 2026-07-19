from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from policies.base_policy import BasePolicy


class PermissionPolicy(BasePolicy):
    """Restricts tools according to the requesting user's role."""

    ROLE_PERMISSIONS = {
        "guest": {
            "get_repository",
            "list_repositories",
            "list_issues",
            "get_issue",
        },
        "developer": {
            "get_repository",
            "list_repositories",
            "list_issues",
            "get_issue",
            "create_issue",
            "update_issue",
            "create_branch",
            "create_pull_request",
        },
        "manager": {
            "get_repository",
            "list_repositories",
            "list_issues",
            "get_issue",
            "create_issue",
            "update_issue",
            "create_branch",
            "create_pull_request",
            "merge_pull_request",
            "add_repository_collaborator",
        },
        "admin": {
            "*",
        },
    }

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision | None:
        user_role = getattr(request, "user_role", None)

        # Until Orion supplies role information, this policy has no opinion.
        if user_role is None:
            return None

        normalized_role = str(user_role).lower()
        allowed_tools = self.ROLE_PERMISSIONS.get(normalized_role)

        if allowed_tools is None:
            return GuardDecision(
                action=GuardAction.BLOCK,
                reason=f"Unknown user role '{user_role}'.",
                policy="permission_policy",
            )

        if "*" in allowed_tools:
            return None

        if request.tool_name in allowed_tools:
            return None

        return GuardDecision(
            action=GuardAction.BLOCK,
            reason=(
                f"Role '{normalized_role}' does not have permission to use "
                f"the tool '{request.tool_name}'."
            ),
            policy="permission_policy",
        )
