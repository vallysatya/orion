from container import container


class FakeToolContext:

    def __init__(self):
        self.state = {}


def test_memory_write_creates_trace_events():

    container.trace_service.clear()

    tool_context = FakeToolContext()

    container.memory_service.set(
        tool_context=tool_context,
        key="risk_score",
        value=90,
    )

    events = container.trace_service.get_trace().events

    event_names = [
        event.event
        for event in events
    ]

    assert "MemoryWriteRequested" in event_names
    assert "StorageDecisionMade" in event_names
    assert "SessionValueWritten" in event_names
