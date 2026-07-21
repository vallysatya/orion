from collections.abc import Sequence

from errors import GuardEvaluationError, OrionError
from models.guard_decision import GuardAction, GuardDecision
from models.guard_request import GuardRequest
from observability.metrics.metrics_service import MetricsService
from observability.trace_service import TraceService
from policies.base_policy import BasePolicy

_OUTCOME_EVENTS = {
    GuardAction.ALLOW: "Allowed",
    GuardAction.BLOCK: "Blocked",
    GuardAction.REQUIRE_APPROVAL: "ApprovalRequired",
}

_RISK_SCORES = {
    GuardAction.ALLOW: 10,
    GuardAction.REQUIRE_APPROVAL: 60,
    GuardAction.BLOCK: 100,
}


class GuardService:
    """Coordinates Orion security policies."""

    def __init__(
        self,
        policies: Sequence[BasePolicy],
        trace_service: TraceService,
        metrics_service: MetricsService,
    ):
        self._policies = list(policies)
        self._trace_service = trace_service
        self._metrics_service = metrics_service

    @property
    def policies(self) -> tuple[BasePolicy, ...]:
        """Return the policies evaluated by this guard, in order."""
        return tuple(self._policies)

    def evaluate(
        self,
        request: GuardRequest,
    ) -> GuardDecision:

        tool_name = request.tool_name

        self._trace_service.record(
            component="GuardService",
            event="GuardCheckRequested",
            metadata={
                "tool": tool_name,
            },
        )

        try:
            for policy in self._policies:
                policy_name = policy.__class__.__name__
                self._trace_service.record(
                    component="GuardService",
                    event="PolicyEvaluationStarted",
                    metadata={
                        "policy": policy_name,
                        "tool": tool_name,
                    },
                )

                try:
                    decision = policy.evaluate(request)
                except OrionError:
                    raise
                except Exception as exc:
                    self._trace_service.record(
                        component="GuardService",
                        event="PolicyEvaluationFailed",
                        metadata={
                            "policy": policy_name,
                            "tool": tool_name,
                            "error_type": type(exc).__name__,
                        },
                    )
                    raise GuardEvaluationError(
                        f"Policy evaluation failed: {policy_name}",
                        tool_name=tool_name,
                        policy=policy_name,
                    ) from exc

                if decision is not None:
                    self._trace_service.record(
                        component="GuardService",
                        event="PolicyMatched",
                        metadata={
                            "policy": policy_name,
                            "tool": tool_name,
                            "decision": decision.action.value,
                        },
                    )
                    return self._finalize(tool_name, decision)

            decision = GuardDecision(
                action=GuardAction.ALLOW,
                reason="Tool execution allowed.",
                policy="default_policy",
            )
            return self._finalize(tool_name, decision)
        except GuardEvaluationError:
            raise
        except OrionError:
            raise
        except Exception as exc:
            self._trace_service.record(
                component="GuardService",
                event="GuardEvaluationFailed",
                metadata={
                    "tool": tool_name,
                    "error_type": type(exc).__name__,
                },
            )
            raise GuardEvaluationError(
                "Guard evaluation failed",
                tool_name=tool_name,
            ) from exc

    def _finalize(
        self,
        tool_name: str,
        decision: GuardDecision,
    ) -> GuardDecision:
        self._trace_service.record(
            component="GuardService",
            event="GuardDecisionMade",
            metadata={
                "tool": tool_name,
                "decision": decision.action.value,
                "risk_score": _RISK_SCORES.get(decision.action, 0),
                "policy": decision.policy,
            },
        )
        self._trace_service.record(
            component="GuardService",
            event=_OUTCOME_EVENTS[decision.action],
            metadata={
                "tool": tool_name,
                "decision": decision.action.value,
            },
        )

        if decision.action == GuardAction.BLOCK:
            self._metrics_service.record_tool_blocked()
        elif decision.action == GuardAction.REQUIRE_APPROVAL:
            self._metrics_service.record_tool_approval_required()
        else:
            self._metrics_service.record_tool_allowed()

        return decision
