from observability.trace_event import TraceEvent

event = TraceEvent(
    component="GitHubAgent",
    event="ToolCalled",
    metadata={
        "tool": "create_issue",
        "repository": "orion",
    },
)

print(event)
