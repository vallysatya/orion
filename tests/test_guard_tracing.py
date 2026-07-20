from container import container
from models.guard_request import GuardRequest


def test_guard_evaluation_creates_trace_events():

    container.trace_service.clear()

    decision = container.guard_service.evaluate(
        GuardRequest(
            request_id="trace-test-001",
            user_id="test-user",
            session_id="test-session",
            tool_name="delete_repository",
            arguments={},
        ),
    )

    events = container.trace_service.get_trace().events
    event_names = [event.event for event in events]

    assert "GuardCheckRequested" in event_names
    assert "PolicyEvaluationStarted" in event_names
    assert "PolicyMatched" in event_names
    assert "GuardDecisionMade" in event_names
    assert "Blocked" in event_names
    assert decision.action.value == "block"
