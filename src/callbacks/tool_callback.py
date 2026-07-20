"""
ADK tool callbacks wired to Orion GuardService + metrics.

Flow:
  before_tool_callback
       ↓
  GuardRequest → GuardService → GuardDecision
       ↓
  ALLOW  → record tool started → return None → after_tool_callback
  BLOCK / REQUIRE_APPROVAL → return dict (tool skipped)
"""

from __future__ import annotations

import time
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

_OUTCOME_EVENTS = {
    GuardAction.ALLOW: "ToolAllowed",
    GuardAction.BLOCK: "ToolBlocked",
    GuardAction.REQUIRE_APPROVAL: "ToolApprovalRequired",
}

_TOOL_START_STATE_KEY = "_orion_tool_started_at_ms"


def before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> dict[str, Any] | None:
    """Evaluate every tool call through Orion Guard before execution."""

    trace = container.trace_service
    metrics = container.metrics_service
    memory = container.memory_service

    trace.record(
        component="ToolCallback",
        event="ToolCallbackStarted",
        metadata={
            "tool": tool.name,
            "agent": getattr(tool_context, "agent_name", None),
        },
    )

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

    trace.record(
        component="ToolCallback",
        event=_OUTCOME_EVENTS[decision.action],
        metadata={
            "tool": tool.name,
            "decision": decision.action.value,
            "policy": decision.policy,
        },
    )

    if decision.action == GuardAction.ALLOW:
        metrics.record_tool_started()
        tool_context.state[_TOOL_START_STATE_KEY] = time.perf_counter()
        return None

    return {
        "status": decision.action.value,
        "reason": decision.reason,
        "policy": decision.policy,
        "tool_name": tool.name,
    }


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any],
) -> dict[str, Any] | None:
    """Record tool execution outcome metrics after a tool returns."""

    metrics = container.metrics_service
    trace = container.trace_service

    started = tool_context.state.pop(_TOOL_START_STATE_KEY, None)
    duration_ms = None
    if isinstance(started, (int, float)):
        duration_ms = (time.perf_counter() - float(started)) * 1000

    if isinstance(tool_response, dict) and tool_response.get("status") in {
        GuardAction.BLOCK.value,
        GuardAction.REQUIRE_APPROVAL.value,
    }:
        return None

    if isinstance(tool_response, dict) and tool_response.get("error"):
        metrics.record_tool_failed(duration_ms)
        trace.record(
            component="ToolCallback",
            event="ToolExecutionFailed",
            metadata={"tool": tool.name},
        )
        return None

    metrics.record_tool_succeeded(duration_ms)
    trace.record(
        component="ToolCallback",
        event="ToolExecutionSucceeded",
        metadata={"tool": tool.name},
    )
    return None
