from dataclasses import dataclass, field

from observability.trace_event import TraceEvent


@dataclass
class Trace:
    """
    Represents the complete execution trace for a single request.
    """

    events: list[TraceEvent] = field(default_factory=list)

    def add_event(
        self,
        event: TraceEvent,
    ) -> None:
        """
        Add a new event to the trace.
        """
        self.events.append(event)

    def clear(self) -> None:
        """
        Remove all events from the trace.
        """
        self.events.clear()

    def __len__(self) -> int:
        """
        Return the number of recorded events.
        """
        return len(self.events)
