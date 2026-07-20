from memory.memory_policy_engine import MemoryPolicyEngine
from memory.policies.dual_memory_policy import DualMemoryPolicy
from memory.policies.persistence_policy import PersistencePolicy
from memory.policies.session_policy import SessionPolicy


engine = MemoryPolicyEngine(
    policies=[
        DualMemoryPolicy(),
        PersistencePolicy(),
        SessionPolicy(),
    ]
)


tests = [
    ("user_name", "Sriram"),
    ("risk_score", 90),
    ("default_repository", "orion"),
    ("unknown_key", "something"),
]


for key, value in tests:

    decision = engine.decide(
        key=key,
        value=value,
    )

    print(
        key,
        "->",
        decision.storage,
    )
