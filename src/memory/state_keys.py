from enum import StrEnum


class StateKey(StrEnum):
    # GitHub context
    CURRENT_REPOSITORY = "current_repository"

    # Security context
    USER_ROLE = "user_role"
    ENVIRONMENT = "environment"
    RISK_SCORE = "risk_score"
    LAST_TOOL = "last_tool"
    LAST_SECURITY_DECISION = "last_security_decision"
    APPROVAL_REQUIRED = "approval_required"

    # General user context
    USER_NAME = "user_name"
    PREFERRED_LANGUAGE = "preferred_language"
    EXPLANATION_STYLE = "explanation_style"
