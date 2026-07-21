from unittest.mock import Mock

from agents.github_agent.clients.github_client import GitHubClient
from errors import GitHubIntegrationError
from observability.trace import Trace
from observability.trace_service import TraceService


def test_get_license_treats_404_as_missing_license():
    client = GitHubClient(trace_service=TraceService(trace=Trace()))
    response = Mock()
    response.status_code = 404
    response.text = "Not Found"
    response.content = b"Not Found"
    client._client = Mock()
    client._client.request.return_value = response

    result = client.get_license("owner", "repo")

    assert result["name"] is None
    assert "No license" in result["message"]


def test_get_license_rethrows_non_404():
    client = GitHubClient(trace_service=TraceService(trace=Trace()))
    response = Mock()
    response.status_code = 500
    response.text = "error"
    response.content = b"error"
    client._client = Mock()
    client._client.request.return_value = response

    try:
        client.get_license("owner", "repo")
        assert False, "expected GitHubIntegrationError"
    except GitHubIntegrationError as exc:
        assert exc.status_code == 500
