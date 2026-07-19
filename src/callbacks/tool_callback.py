"""
ADK before_tool callback wired to Orion GuardService.

Flow:
  ToolContext + args
       ↓
  before_tool_callback
       ↓
  GuardRequest → GuardService → GuardDecision
       ↓
  MemoryService records decision
       ↓
  ALLOW  → return None  (tool executes)
  BLOCK / REQUIRE_APPROVAL → return dict (tool skipped)
"""

from __future__ import annotations

from typing import Any

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from container import container
from models.guard_decision import GuardAction
from models.guard_request import GuardRequest

_RISK_SCORES = {
    GuardAction.ALLOW.value: 10,
    GuardAction.REQUIRE_APPROVAL.value: 60,
    GuardAction.BLOCK.value: 100,
}


def before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> dict[str, Any] | None:
    """Evaluate every tool call through Orion Guard before execution."""

    memory = container.memory_service
    remembered_environment = memory.get_environment(tool_context)

    request = GuardRequest(
        request_id=getattr(
            tool_context,
            "invocation_id",
            "unknown-request",
        ),
        user_id="unknown-user",
        session_id="unknown-session",
        tool_name=tool.name,
        arguments=args,
        agent_name=getattr(
            tool_context,
            "agent_name",
            None,
        ),
        environment=remembered_environment
        or getattr(
            tool_context,
            "environment",
            "development",
        ),
    )

    decision = container.guard_service.evaluate(request)

    memory.set_last_tool(tool_context, tool.name)
    memory.set_last_security_decision(
        tool_context,
        decision.action.value,
    )
    memory.set_approval_required(
        tool_context,
        decision.action == GuardAction.REQUIRE_APPROVAL,
    )
    memory.set_risk_score(
        tool_context,
        _RISK_SCORES.get(decision.action.value, 0),
    )

    if decision.action == GuardAction.ALLOW:
        return None

    return {
        "status": decision.action.value,
        "reason": decision.reason,
        "policy": decision.policy,
        "tool_name": tool.name,
    }
