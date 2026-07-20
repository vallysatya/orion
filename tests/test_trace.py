from observability.trace import Trace
from observability.trace_event import TraceEvent

trace = Trace()

trace.add_event(
    TraceEvent(
        component="Coordinator",
        event="RequestStarted",
    )
)

trace.add_event(
    TraceEvent(
        component="GitHubAgent",
        event="ToolCalled",
    )
)

print(len(trace))

print(trace.events)
