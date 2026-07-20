from observability.exporters.console_exporter import ConsoleExporter
from observability.exporters.json_exporter import JsonExporter
from observability.trace import Trace
from observability.trace_service import TraceService

trace = Trace()

service = TraceService(trace)

service.record(
    component="Coordinator",
    event="RequestStarted",
)

service.record(
    component="GitHubAgent",
    event="ToolCalled",
    metadata={
        "tool": "create_issue",
    },
)

ConsoleExporter().export(
    service.get_trace()
)

JsonExporter().export(
    service.get_trace()
)
