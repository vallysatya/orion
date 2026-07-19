from google.adk.tools.tool_context import ToolContext

from container import container


ALLOWED_ENVIRONMENTS = {
    "development",
    "staging",
    "production",
}

ALLOWED_ROLES = {
    "viewer",
    "developer",
    "maintainer",
    "admin",
}


def remember_user_role(
    role: str,
    tool_context: ToolContext,
) -> dict:
    """
    Remember the user's claimed role for the current session.

    This value is contextual information only. It does not independently
    prove that the user has the claimed permissions.
    """
    normalized_role = role.strip().lower()

    if normalized_role not in ALLOWED_ROLES:
        return {
            "status": "error",
            "message": (
                "Unsupported role. Allowed roles are: "
                + ", ".join(sorted(ALLOWED_ROLES))
            ),
        }

    container.memory_service.set_user_role(
        tool_context,
        normalized_role,
    )

    return {
        "status": "success",
        "user_role": normalized_role,
    }


def get_user_role(
    tool_context: ToolContext,
) -> dict:
    """Return the user role remembered for the current session."""
    role = container.memory_service.get_user_role(tool_context)

    if role is None:
        return {
            "status": "not_found",
            "message": "No user role has been remembered.",
        }

    return {
        "status": "success",
        "user_role": role,
    }


def remember_environment(
    environment: str,
    tool_context: ToolContext,
) -> dict:
    """Remember the active environment."""
    normalized_environment = environment.strip().lower()

    if normalized_environment not in ALLOWED_ENVIRONMENTS:
        return {
            "status": "error",
            "message": (
                "Unsupported environment. Allowed environments are: "
                + ", ".join(sorted(ALLOWED_ENVIRONMENTS))
            ),
        }

    container.memory_service.set_environment(
        tool_context,
        normalized_environment,
    )

    return {
        "status": "success",
        "environment": normalized_environment,
    }


def get_environment(
    tool_context: ToolContext,
) -> dict:
    """Return the active environment."""
    environment = container.memory_service.get_environment(
        tool_context,
    )

    return {
        "status": "success",
        "environment": environment,
    }


def get_last_security_decision(
    tool_context: ToolContext,
) -> dict:
    """Return the most recent Orion Guard security decision."""
    decision = container.memory_service.get_last_security_decision(
        tool_context,
    )

    if decision is None:
        return {
            "status": "not_found",
            "message": "No security decision has been recorded.",
        }

    return {
        "status": "success",
        "decision": decision,
        "risk_score": container.memory_service.get_risk_score(
            tool_context,
        ),
        "approval_required": (
            container.memory_service.is_approval_required(
                tool_context,
            )
        ),
        "last_tool": container.memory_service.get_last_tool(
            tool_context,
        ),
    }
