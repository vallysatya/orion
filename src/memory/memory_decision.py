from dataclasses import dataclass
from enum import StrEnum


class MemoryStorage(StrEnum):
    SESSION = "session"
    PERSISTENT = "persistent"
    BOTH = "both"


@dataclass
class MemoryDecision:
    storage: MemoryStorage
