from typing import Any

from google.adk.tools.tool_context import ToolContext

from memory.state_keys import StateKey


class MemoryService:
    """
    Orion abstraction over ADK session state.

    Agents and tools should use this service instead of accessing
    tool_context.state directly.
    """

    # ------------------------------------------------------------------
    # Generic operations
    # ------------------------------------------------------------------

    def get(
        self,
        tool_context: ToolContext,
        key: StateKey,
        default: Any = None,
    ) -> Any:
        return tool_context.state.get(key.value, default)

    def set(
        self,
        tool_context: ToolContext,
        key: StateKey,
        value: Any,
    ) -> None:
        tool_context.state[key.value] = value

    def delete(
        self,
        tool_context: ToolContext,
        key: StateKey,
    ) -> None:
        # ADK State has no public pop; clear committed + delta maps.
        key_name = key.value
        value = getattr(tool_context.state, "_value", None)
        delta = getattr(tool_context.state, "_delta", None)
        if isinstance(value, dict):
            value.pop(key_name, None)
        if isinstance(delta, dict):
            delta.pop(key_name, None)

    def exists(
        self,
        tool_context: ToolContext,
        key: StateKey,
    ) -> bool:
        return key.value in tool_context.state

    def clear(self, tool_context: ToolContext) -> None:
        # ADK State has no public clear(); empty committed + delta maps.
        value = getattr(tool_context.state, "_value", None)
        delta = getattr(tool_context.state, "_delta", None)
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
