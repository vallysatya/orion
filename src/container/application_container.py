from dataclasses import dataclass

from memory.memory_service import MemoryService
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
    memory_service: MemoryService


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
    memory_service = MemoryService()

    return ApplicationContainer(
        guard_service=guard_service,
        memory_service=memory_service,
    )
