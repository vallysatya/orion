from dataclasses import dataclass

from policies.approval_policy import ApprovalPolicy
from policies.destructive_action_policy import DestructiveActionPolicy
from policies.environment_policy import EnvironmentPolicy
from policies.permission_policy import PermissionPolicy
from policies.pii_policy import PIIPolicy
from policies.prompt_injection_policy import PromptInjectionPolicy
from services.guard_service import GuardService


@dataclass(frozen=True)
class ApplicationContainer:
    """Holds Orion application-wide services."""

    guard_service: GuardService


def build_application_container() -> ApplicationContainer:
    """Create and connect Orion services."""

    policies = [
        PromptInjectionPolicy(),
        PIIPolicy(),
        PermissionPolicy(),
        EnvironmentPolicy(),
        DestructiveActionPolicy(),
        ApprovalPolicy(),
    ]

    guard_service = GuardService(
        policies=policies,
    )

    return ApplicationContainer(
        guard_service=guard_service,
    )
