from typing import Any

from observability.trace import Trace
from observability.trace_event import TraceEvent


class TraceService:
    """
    Records events into the current execution trace.
    """

    def __init__(
        self,
        trace: Trace,
    ):
        self._trace = trace

    def record(
        self,
        component: str,
        event: str,
        metadata: dict[str, Any] | None = None,
    ) -> TraceEvent:
        """
        Create and store a new trace event.
        """

        trace_event = TraceEvent(
            component=component,
            event=event,
            metadata=metadata or {},
        )

        self._trace.add_event(
            trace_event,
        )

        return trace_event

    def get_trace(self) -> Trace:
        """
        Return the current trace.
        """
        return self._trace

    def clear(self) -> None:
        """
        Remove all events from the current trace.
        """
        self._trace.clear()
