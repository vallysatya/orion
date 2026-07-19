from enum import Enum
from dataclasses import dataclass


class GuardAction(Enum):
    ALLOW = "allow"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"


@dataclass(frozen=True)
class GuardDecision:
    action: GuardAction
    reason: str
    policy: str | None = None
