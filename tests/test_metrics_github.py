from unittest.mock import Mock

from agents.github_agent.clients.github_client import GitHubClient
from observability.metrics import MetricNames, MetricsRegistry, MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService


def test_github_client_records_request_metrics():
    metrics = MetricsService(registry=MetricsRegistry())
    client = GitHubClient(
        trace_service=TraceService(trace=Trace()),
        metrics_service=metrics,
    )

    response = Mock()
    response.status_code = 200
    response.content = b'{"ok": true}'
    response.json.return_value = {"ok": True}
    client._client = Mock()
    client._client.request.return_value = response

    client._request("GET", "/user")

    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_TOTAL) == 1
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_SUCCEEDED) == 1
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_FAILED) == 0
    assert (
        metrics.get_average_timing(MetricNames.GITHUB_REQUEST_DURATION_MS)
        >= 0
    )


def test_github_client_records_failed_request_metrics():
    metrics = MetricsService(registry=MetricsRegistry())
    client = GitHubClient(
        trace_service=TraceService(trace=Trace()),
        metrics_service=metrics,
    )

    response = Mock()
    response.status_code = 500
    response.text = "error"
    response.content = b"error"
    client._client = Mock()
    client._client.request.return_value = response

    try:
        client._request("GET", "/boom")
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass

    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_TOTAL) == 1
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_SUCCEEDED) == 0
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_FAILED) == 1
    assert len(metrics.get_timings(MetricNames.GITHUB_REQUEST_DURATION_MS)) == 1
