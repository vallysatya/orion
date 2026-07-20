from container import container
from models.guard_decision import GuardAction
from test_tool_callback import _run_callback


def test_tool_callback_records_blocked_trace_events():
    container.trace_service.clear()

    result = _run_callback(
        "delete_repository",
        {"owner": "google", "repo": "orion"},
    )

    assert result is not None
    assert result["status"] == GuardAction.BLOCK.value

    event_names = [event.event for event in container.trace_service.get_trace().events]
    assert "ToolCallbackStarted" in event_names
    assert "GuardCheckRequested" in event_names
    assert "ToolBlocked" in event_names


def test_tool_callback_records_allowed_trace_events():
    container.trace_service.clear()

    result = _run_callback(
        "get_repository",
        {"owner": "google", "repo": "adk-python"},
    )

    assert result is None

    event_names = [event.event for event in container.trace_service.get_trace().events]
    assert "ToolCallbackStarted" in event_names
    assert "ToolAllowed" in event_names
