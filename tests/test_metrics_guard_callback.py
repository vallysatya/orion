from unittest.mock import Mock

from container import container
from models.guard_decision import GuardAction
from models.guard_request import GuardRequest
from observability.metrics import MetricNames
from callbacks.tool_callback import after_tool_callback
from test_tool_callback import _run_callback


def test_guard_records_blocked_metric():
    container.metrics_service.clear()

    decision = container.guard_service.evaluate(
        GuardRequest(
            request_id="metrics-guard-001",
            user_id="test-user",
            session_id="test-session",
            tool_name="delete_repository",
            arguments={},
        ),
    )

    assert decision.action == GuardAction.BLOCK
    assert (
        container.metrics_service.get_counter(MetricNames.TOOL_CALLS_BLOCKED)
        == 1
    )


def test_guard_records_allowed_metric():
    container.metrics_service.clear()

    decision = container.guard_service.evaluate(
        GuardRequest(
            request_id="metrics-guard-002",
            user_id="test-user",
            session_id="test-session",
            tool_name="get_repository",
            arguments={},
        ),
    )

    assert decision.action == GuardAction.ALLOW
    assert (
        container.metrics_service.get_counter(MetricNames.TOOL_CALLS_ALLOWED)
        == 1
    )


def test_blocked_tool_does_not_count_as_execution():
    container.metrics_service.clear()

    result = _run_callback(
        "delete_repository",
        {"owner": "google", "repo": "orion"},
    )

    assert result is not None
    assert result["status"] == GuardAction.BLOCK.value
    assert (
        container.metrics_service.get_counter(
            MetricNames.TOOL_EXECUTIONS_TOTAL
        )
        == 0
    )
    assert (
        container.metrics_service.get_counter(MetricNames.TOOL_CALLS_BLOCKED)
        == 1
    )


def test_allowed_tool_counts_execution_start():
    container.metrics_service.clear()

    result = _run_callback(
        "get_repository",
        {"owner": "google", "repo": "adk-python"},
    )

    assert result is None
    assert (
        container.metrics_service.get_counter(
            MetricNames.TOOL_EXECUTIONS_TOTAL
        )
        == 1
    )
    assert (
        container.metrics_service.get_counter(MetricNames.TOOL_CALLS_ALLOWED)
        == 1
    )


def test_after_tool_callback_records_success():
    container.metrics_service.clear()

    tool = Mock()
    tool.name = "get_repository"
    tool_context = Mock()
    tool_context.state = {"_orion_tool_started_at_ms": 0.0}

    after_tool_callback(
        tool=tool,
        args={},
        tool_context=tool_context,
        tool_response={"ok": True},
    )

    assert (
        container.metrics_service.get_counter(
            MetricNames.TOOL_EXECUTIONS_SUCCEEDED
        )
        == 1
    )


def test_tool_callback_records_approval_metric():
    container.metrics_service.clear()

    result = _run_callback("merge_pull_request", {"pr_number": 12})

    assert result is not None
    assert result["status"] == GuardAction.REQUIRE_APPROVAL.value
    assert (
        container.metrics_service.get_counter(
            MetricNames.TOOL_CALLS_APPROVAL_REQUIRED
        )
        == 1
    )
