from dataclasses import dataclass
from pathlib import Path

from memory.memory_policy_engine import MemoryPolicyEngine
from memory.memory_service import MemoryService
from memory.persistent_memory import PersistentMemory
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy
from memory.sqlite_memory import SQLiteMemory
from policies.approval_policy import ApprovalPolicy
from policies.destructive_action_policy import DestructiveActionPolicy
from policies.environment_policy import EnvironmentPolicy
from policies.permission_policy import PermissionPolicy
from policies.pii_policy import PIIPolicy
from policies.prompt_injection_policy import PromptInjectionPolicy
from services.guard_service import GuardService

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_MEMORY_DB = _PROJECT_ROOT / "orion_memory.db"


@dataclass(frozen=True)
class ApplicationContainer:
    """Holds Orion application-wide services."""

    guard_service: GuardService
    persistent_memory: PersistentMemory
    memory_policy_engine: MemoryPolicyEngine
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
    persistent_memory = SQLiteMemory(
        database_path=str(_DEFAULT_MEMORY_DB),
    )
    memory_policy_engine = MemoryPolicyEngine(
        policies=[
            DualMemoryPolicy(),
            PersistencePolicy(),
            SessionPolicy(),
        ],
    )
    memory_service = MemoryService(
        persistent_memory=persistent_memory,
        policy_engine=memory_policy_engine,
    )

    return ApplicationContainer(
        guard_service=guard_service,
        persistent_memory=persistent_memory,
        memory_policy_engine=memory_policy_engine,
        memory_service=memory_service,
    )
