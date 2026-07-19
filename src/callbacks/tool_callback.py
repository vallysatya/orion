"""
ADK before_tool callback wired to Orion GuardService.

Flow:
  ToolContext + args
       ↓
  before_tool_callback
       ↓
  GuardRequest → GuardService → GuardDecision
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


def before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> dict[str, Any] | None:
    """Evaluate every tool call through Orion Guard before execution."""

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
        environment=getattr(
            tool_context,
            "environment",
            "development",
        ),
    )

    decision = container.guard_service.evaluate(request)

    if decision.action == GuardAction.ALLOW:
        return None

    return {
        "status": decision.action.value,
        "reason": decision.reason,
        "policy": decision.policy,
        "tool_name": tool.name,
    }
