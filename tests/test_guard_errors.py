"""GuardService error-wrapping tests."""

from __future__ import annotations

from models.guard_decision import GuardDecision
from models.guard_request import GuardRequest
from observability.metrics import MetricsRegistry, MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService
from policies.base_policy import BasePolicy
from services.guard_service import GuardService
from errors import GuardEvaluationError, OrionError


class _BoomPolicy(BasePolicy):
    def evaluate(self, request: GuardRequest) -> GuardDecision | None:
        raise ValueError("policy exploded")


def test_guard_wraps_policy_failures():
    trace = Trace()
    guard = GuardService(
        policies=[_BoomPolicy()],
        trace_service=TraceService(trace=trace),
        metrics_service=MetricsService(MetricsRegistry()),
    )

    try:
        guard.evaluate(
            GuardRequest(
                request_id="g1",
                user_id="u",
                session_id="s",
                tool_name="get_repository",
                arguments={},
            )
        )
        assert False, "expected GuardEvaluationError"
    except GuardEvaluationError as exc:
        assert isinstance(exc, OrionError)
        assert exc.tool_name == "get_repository"
        assert exc.policy == "_BoomPolicy"
        assert isinstance(exc.__cause__, ValueError)

    assert "PolicyEvaluationFailed" in [e.event for e in trace.events]
