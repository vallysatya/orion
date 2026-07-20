from container import container


def test_container_trace_service_records_events():

    container.trace_service.clear()

    event = container.trace_service.record(
        component="TestComponent",
        event="TestEvent",
        metadata={
            "status": "working",
        },
    )

    trace = container.trace_service.get_trace()

    assert len(trace) == 1
    assert event.component == "TestComponent"
    assert event.event == "TestEvent"
    assert event.metadata["status"] == "working"


def test_container_shares_one_trace_instance():

    assert (
        container.trace_service.get_trace()
        is container.trace
    )
