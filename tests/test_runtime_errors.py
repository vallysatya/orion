"""AgentRunner error-wrapping tests."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from errors import OrionRuntimeError
from models.session_info import SessionInfo
from observability.metrics import MetricNames, MetricsRegistry, MetricsService
from observability.trace import Trace
from observability.trace_service import TraceService
from runtime.runner import AgentRunner


def test_runtime_wraps_unexpected_failures():
    metrics = MetricsService(MetricsRegistry())
    session_adapter = MagicMock()
    session_adapter.ensure_session = AsyncMock(
        side_effect=RuntimeError("adk broke"),
    )
    session_adapter.service = MagicMock()

    with (
        patch("runtime.runner.App") as mock_app,
        patch("runtime.runner.Runner") as mock_runner_cls,
        patch("runtime.runner.InMemoryArtifactService"),
        patch("runtime.runner.InMemoryMemoryService"),
    ):
        mock_app.return_value = MagicMock()
        mock_runner = MagicMock()
        mock_runner.app_name = "orion"
        mock_runner.close = AsyncMock()
        mock_runner_cls.return_value = mock_runner

        runner = AgentRunner(
            agent=MagicMock(name="orion_coordinator"),
            session_adapter=session_adapter,
            trace_service=TraceService(trace=Trace()),
            metrics_service=metrics,
        )

        session = SessionInfo(session_id="s1", user_id="u1", title="t")

        try:
            asyncio.run(runner.run_message("hello", session=session))
            assert False, "expected OrionRuntimeError"
        except OrionRuntimeError as exc:
            assert exc.operation == "stream_message"
            assert exc.session_id == "s1"
            assert isinstance(exc.__cause__, RuntimeError)

    assert metrics.get_counter(MetricNames.REQUESTS_FAILED) == 1
