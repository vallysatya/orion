from observability.trace import Trace
from observability.trace_service import TraceService


trace = Trace()

trace_service = TraceService(
    trace=trace,
)

trace_service.record(
    component="Coordinator",
    event="RequestStarted",
    metadata={
        "request": "Create an issue",
    },
)

trace_service.record(
    component="GitHubAgent",
    event="ToolSelected",
    metadata={
        "tool": "create_issue",
    },
)

print(len(trace_service.get_trace()))

for event in trace_service.get_trace().events:
    print(
        event.component,
        event.event,
        event.metadata,
    )
