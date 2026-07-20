import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from models.session_info import SessionInfo
from observability.metrics import MetricNames, MetricsRegistry, MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService
from runtime.runner import AgentRunner


def test_runtime_records_request_metrics():
    metrics = MetricsService(registry=MetricsRegistry())
    session_adapter = MagicMock()
    adk_session = MagicMock()
    adk_session.user_id = "user-1"
    adk_session.id = "adk-session-1"
    session_adapter.ensure_session = AsyncMock(return_value=adk_session)
    session_adapter.service = MagicMock()

    async def _fake_run_async(**kwargs):
        if False:
            yield None
        return
        yield  # pragma: no cover

    with (
        patch("runtime.runner.App") as mock_app,
        patch("runtime.runner.Runner") as mock_runner_cls,
        patch("runtime.runner.InMemoryArtifactService"),
        patch("runtime.runner.InMemoryMemoryService"),
    ):
        mock_app.return_value = MagicMock()
        mock_runner = MagicMock()
        mock_runner.app_name = "orion"
        mock_runner.run_async = _fake_run_async
        mock_runner.close = AsyncMock()
        mock_runner_cls.return_value = mock_runner

        runner = AgentRunner(
            agent=MagicMock(name="orion_coordinator"),
            session_adapter=session_adapter,
            trace_service=TraceService(trace=Trace()),
            metrics_service=metrics,
        )

        session = SessionInfo(
            session_id="session-1",
            user_id="user-1",
            title="Test",
        )
        asyncio.run(runner.run_message("hello", session=session))

    assert metrics.get_counter(MetricNames.REQUESTS_TOTAL) == 1
    assert metrics.get_counter(MetricNames.REQUESTS_SUCCEEDED) == 1
    assert metrics.get_counter(MetricNames.REQUESTS_FAILED) == 0
    assert metrics.get_average_timing(MetricNames.REQUEST_DURATION_MS) >= 0
