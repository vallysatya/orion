from container import container
from observability.metrics import MetricNames


def test_container_exposes_metrics_service():
    assert container.metrics_service is not None
    assert container.metrics_registry is not None


def test_container_shares_one_metrics_registry():
    container.metrics_service.clear()
    container.metrics_service.increment(MetricNames.REQUESTS_TOTAL)

    assert (
        container.metrics_registry.get_counter(MetricNames.REQUESTS_TOTAL)
        == 1
    )
    container.metrics_service.clear()
