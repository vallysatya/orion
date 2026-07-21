from unittest.mock import Mock

from agents.github_agent.clients.github_client import GitHubClient
from errors import GitHubIntegrationError
from observability.trace import Trace
from observability.trace_service import TraceService


def test_github_client_records_successful_request():
    trace = Trace()
    trace_service = TraceService(trace=trace)
    client = GitHubClient(trace_service=trace_service)

    response = Mock()
    response.status_code = 200
    response.content = b'{"ok": true}'
    response.json.return_value = {"ok": True}
    client._client = Mock()
    client._client.request.return_value = response

    result = client._request("GET", "/user")

    assert result == {"ok": True}
    event_names = [event.event for event in trace.events]
    assert "GitHubApiRequestStarted" in event_names
    assert "GitHubApiRequestSucceeded" in event_names


def test_github_client_records_failed_request():
    trace = Trace()
    trace_service = TraceService(trace=trace)
    client = GitHubClient(trace_service=trace_service)

    response = Mock()
    response.status_code = 404
    response.text = "Not Found"
    response.content = b"Not Found"
    client._client = Mock()
    client._client.request.return_value = response

    try:
        client._request("GET", "/repos/missing/repo")
        assert False, "expected GitHubIntegrationError"
    except GitHubIntegrationError as exc:
        assert exc.status_code == 404

    event_names = [event.event for event in trace.events]
    assert "GitHubApiRequestStarted" in event_names
    assert "GitHubApiRequestFailed" in event_names
