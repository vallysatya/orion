import pytest

from observability.metrics import MetricsRegistry, MetricsService


def create_service() -> MetricsService:
    return MetricsService(MetricsRegistry())


def test_increment_counter():
    service = create_service()

    service.increment("requests_total")
    service.increment("requests_total", 2)

    assert service.get_counter("requests_total") == 3


def test_average_timing():
    service = create_service()

    service.record_timing("request_duration_ms", 100)
    service.record_timing("request_duration_ms", 300)

    assert service.get_average_timing("request_duration_ms") == 200


def test_empty_average_returns_zero():
    service = create_service()

    assert service.get_average_timing("missing_metric") == 0.0


def test_request_success_metrics():
    service = create_service()

    service.record_request_started()
    service.record_request_succeeded(250)

    snapshot = service.snapshot()

    assert snapshot.counters["requests_total"] == 1
    assert snapshot.counters["requests_succeeded"] == 1
    assert snapshot.timings["request_duration_ms"] == (250,)


def test_request_failure_metrics():
    service = create_service()

    service.record_request_started()
    service.record_request_failed(180)

    snapshot = service.snapshot()

    assert snapshot.counters["requests_total"] == 1
    assert snapshot.counters["requests_failed"] == 1
    assert snapshot.timings["request_duration_ms"] == (180,)


def test_clear_metrics():
    service = create_service()

    service.increment("requests_total")
    service.record_timing("request_duration_ms", 120)

    service.clear()

    assert service.get_counter("requests_total") == 0
    assert service.get_average_timing("request_duration_ms") == 0.0


def test_negative_increment_is_rejected():
    service = create_service()

    with pytest.raises(ValueError):
        service.increment("requests_total", -1)


def test_domain_helpers():
    service = create_service()

    service.record_tool_allowed()
    service.record_tool_blocked()
    service.record_tool_approval_required()
    service.record_tool_started()
    service.record_tool_succeeded(12.0)
    service.record_memory_hit()
    service.record_memory_miss()
    service.record_memory_write()
    service.record_github_request_started()
    service.record_github_request_succeeded(40.0)
    service.record_github_request_failed(15.0)

    snap = service.snapshot()
    assert snap.counters["tool_calls_allowed"] == 1
    assert snap.counters["tool_calls_blocked"] == 1
    assert snap.counters["tool_executions_succeeded"] == 1
    assert snap.counters["memory_hits"] == 1
    assert snap.counters["github_requests_succeeded"] == 1
    assert snap.counters["github_requests_failed"] == 1
    assert snap.timings["github_request_duration_ms"] == (40.0, 15.0)
    assert snap.timings["tool_duration_ms"] == (12.0,)
