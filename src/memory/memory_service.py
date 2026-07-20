from typing import Any

from google.adk.tools.tool_context import ToolContext

from memory.memory_decision import MemoryStorage
from memory.memory_policy_engine import MemoryPolicyEngine
from memory.persistent_memory import PersistentMemory
from memory.state_keys import StateKey


class MemoryService:
    """
    Orion abstraction over ADK session state and persistent storage.

    Storage destination is decided by MemoryPolicyEngine
    (session, persistent, or both).
    """

    def __init__(
        self,
        persistent_memory: PersistentMemory,
        policy_engine: MemoryPolicyEngine,
    ):
        self._persistent_memory = persistent_memory
        self._policy_engine = policy_engine

    @staticmethod
    def _key_name(key: StateKey | str) -> str:
        return key.value if isinstance(key, StateKey) else key

    @staticmethod
    def _delete_session_key(tool_context: ToolContext, key_name: str) -> None:
        state = tool_context.state
        if isinstance(state, dict):
            state.pop(key_name, None)
            return

        # ADK State has no public pop; clear committed + delta maps.
        value = getattr(state, "_value", None)
        delta = getattr(state, "_delta", None)
        if isinstance(value, dict):
            value.pop(key_name, None)
        if isinstance(delta, dict):
            delta.pop(key_name, None)

    # ------------------------------------------------------------------
    # Generic operations
    # ------------------------------------------------------------------

    def get(
        self,
        tool_context: ToolContext,
        key: StateKey | str,
        default: Any = None,
    ) -> Any:
        key_name = self._key_name(key)
        if key_name in tool_context.state:
            return tool_context.state.get(key_name, default)

        # Hydrate session from persistent storage when available.
        persistent_value = self._persistent_memory.get(key_name)
        if persistent_value is not None:
            tool_context.state[key_name] = persistent_value
            return persistent_value

        return default

    def set(
        self,
        tool_context: ToolContext,
        key: StateKey | str,
        value: Any,
    ) -> None:
        key_name = self._key_name(key)
        decision = self._policy_engine.decide(key=key_name, value=value)

        if decision.storage in {
            MemoryStorage.SESSION,
            MemoryStorage.BOTH,
        }:
            tool_context.state[key_name] = value

        if decision.storage in {
            MemoryStorage.PERSISTENT,
            MemoryStorage.BOTH,
        }:
            self._persistent_memory.set(key_name, value)

    def delete(
        self,
        tool_context: ToolContext,
        key: StateKey | str,
    ) -> None:
        key_name = self._key_name(key)
        decision = self._policy_engine.decide(key=key_name, value=None)

        if decision.storage in {
            MemoryStorage.SESSION,
            MemoryStorage.BOTH,
        }:
            self._delete_session_key(tool_context, key_name)

        if decision.storage in {
            MemoryStorage.PERSISTENT,
            MemoryStorage.BOTH,
        }:
            self._persistent_memory.delete(key_name)

    def exists(
        self,
        tool_context: ToolContext,
        key: StateKey | str,
    ) -> bool:
        key_name = self._key_name(key)
        if key_name in tool_context.state:
            return True
        return self._persistent_memory.exists(key_name)

    def clear(self, tool_context: ToolContext) -> None:
        state = tool_context.state
        if isinstance(state, dict):
            state.clear()
            return

        # ADK State has no public clear(); empty committed + delta maps.
        value = getattr(state, "_value", None)
        delta = getattr(state, "_delta", None)
        if isinstance(value, dict):
            value.clear()
        if isinstance(delta, dict):
            delta.clear()

    # ------------------------------------------------------------------
    # Repository memory
    # ------------------------------------------------------------------

    def get_current_repository(
        self,
        tool_context: ToolContext,
    ) -> str | None:
        return self.get(
            tool_context,
            StateKey.CURRENT_REPOSITORY,
        )

    def set_current_repository(
        self,
        tool_context: ToolContext,
        repository: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.CURRENT_REPOSITORY,
            repository,
        )

    # ------------------------------------------------------------------
    # Security memory
    # ------------------------------------------------------------------

    def get_user_role(
        self,
        tool_context: ToolContext,
    ) -> str | None:
        return self.get(
            tool_context,
            StateKey.USER_ROLE,
        )

    def set_user_role(
        self,
        tool_context: ToolContext,
        role: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.USER_ROLE,
            role,
        )

    def get_environment(
        self,
        tool_context: ToolContext,
    ) -> str:
        return self.get(
            tool_context,
            StateKey.ENVIRONMENT,
            "development",
        )

    def set_environment(
        self,
        tool_context: ToolContext,
        environment: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.ENVIRONMENT,
            environment,
        )

    def get_risk_score(
        self,
        tool_context: ToolContext,
    ) -> int:
        return self.get(
            tool_context,
            StateKey.RISK_SCORE,
            0,
        )

    def set_risk_score(
        self,
        tool_context: ToolContext,
        score: int,
    ) -> None:
        self.set(
            tool_context,
            StateKey.RISK_SCORE,
            score,
        )

    def get_last_tool(
        self,
        tool_context: ToolContext,
    ) -> str | None:
        return self.get(
            tool_context,
            StateKey.LAST_TOOL,
        )

    def set_last_tool(
        self,
        tool_context: ToolContext,
        tool_name: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.LAST_TOOL,
            tool_name,
        )

    def get_last_security_decision(
        self,
        tool_context: ToolContext,
    ) -> str | None:
        return self.get(
            tool_context,
            StateKey.LAST_SECURITY_DECISION,
        )

    def set_last_security_decision(
        self,
        tool_context: ToolContext,
        decision: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.LAST_SECURITY_DECISION,
            decision,
        )

    def is_approval_required(
        self,
        tool_context: ToolContext,
    ) -> bool:
        return self.get(
            tool_context,
            StateKey.APPROVAL_REQUIRED,
            False,
        )

    def set_approval_required(
        self,
        tool_context: ToolContext,
        required: bool,
    ) -> None:
        self.set(
            tool_context,
            StateKey.APPROVAL_REQUIRED,
            required,
        )

    # ------------------------------------------------------------------
    # User preference memory
    # ------------------------------------------------------------------

    def get_user_name(
        self,
        tool_context: ToolContext,
    ) -> str | None:
        return self.get(
            tool_context,
            StateKey.USER_NAME,
        )

    def set_user_name(
        self,
        tool_context: ToolContext,
        name: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.USER_NAME,
            name,
        )

    def get_preferred_language(
        self,
        tool_context: ToolContext,
    ) -> str:
        return self.get(
            tool_context,
            StateKey.PREFERRED_LANGUAGE,
            "English",
        )

    def set_preferred_language(
        self,
        tool_context: ToolContext,
        language: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.PREFERRED_LANGUAGE,
            language,
        )

    def get_explanation_style(
        self,
        tool_context: ToolContext,
    ) -> str:
        return self.get(
            tool_context,
            StateKey.EXPLANATION_STYLE,
            "simple",
        )

    def set_explanation_style(
        self,
        tool_context: ToolContext,
        style: str,
    ) -> None:
        self.set(
            tool_context,
            StateKey.EXPLANATION_STYLE,
            style,
        )

    # ------------------------------------------------------------------
    # Persistent Memory
    # ------------------------------------------------------------------

    def save_preference(
        self,
        key: str,
        value: Any,
    ) -> None:
        decision = self._policy_engine.decide(key=key, value=value)
        if decision.storage in {
            MemoryStorage.PERSISTENT,
            MemoryStorage.BOTH,
        }:
            self._persistent_memory.set(key, value)

    def load_preference(
        self,
        key: str,
    ) -> Any:
        return self._persistent_memory.get(key)

    def delete_preference(
        self,
        key: str,
    ) -> None:
        decision = self._policy_engine.decide(key=key, value=None)
        if decision.storage in {
            MemoryStorage.PERSISTENT,
            MemoryStorage.BOTH,
        }:
            self._persistent_memory.delete(key)

    def preference_exists(
        self,
        key: str,
    ) -> bool:
        return self._persistent_memory.exists(key)
