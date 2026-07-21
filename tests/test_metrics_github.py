from unittest.mock import Mock

from agents.github_agent.clients.github_client import GitHubClient
from errors import GitHubIntegrationError, OrionError
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
        assert False, "expected GitHubIntegrationError"
    except GitHubIntegrationError as exc:
        assert exc.status_code == 500
        assert exc.endpoint == "/boom"

    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_TOTAL) == 1
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_SUCCEEDED) == 0
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_FAILED) == 1
    assert len(metrics.get_timings(MetricNames.GITHUB_REQUEST_DURATION_MS)) == 1


def test_github_client_wraps_transport_errors():
    metrics = MetricsService(registry=MetricsRegistry())
    trace = Trace()
    client = GitHubClient(
        trace_service=TraceService(trace=trace),
        metrics_service=metrics,
    )
    client._client = Mock()
    client._client.request.side_effect = TimeoutError("timed out")

    try:
        client._request("GET", "/user")
        assert False, "expected GitHubIntegrationError"
    except GitHubIntegrationError as exc:
        assert isinstance(exc, OrionError)
        assert isinstance(exc.__cause__, TimeoutError)
        assert exc.method == "GET"
        assert exc.endpoint == "/user"

    assert "GitHubApiRequestFailed" in [e.event for e in trace.events]
    assert metrics.get_counter(MetricNames.GITHUB_REQUESTS_FAILED) == 1
