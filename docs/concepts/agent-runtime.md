# Agent runtime

Orion runs agents through Google ADK, wrapped by `OrionApp` and `AgentRunner`.

## Entry points

| Path | Role |
| --- | --- |
| `orion` console script → `cli.main:main` | Production CLI |
| `src/main.py` | Thin compatibility wrapper calling the CLI |
| `src/orion/agent.py` / `src/orion/main.py` | Legacy placeholder (“Hello from Orion!”) — **not** the runtime |

Use the CLI or import `runtime.app.OrionApp` for real execution.

## OrionApp

`OrionApp`:

1. Validates configuration (`GOOGLE_API_KEY` required when `require_google_api_key=True`)
2. Creates a `SessionManager` for Orion session metadata
3. Creates an `ADKSessionAdapter` (default: ADK `InMemorySessionService`)
4. Builds `AgentRunner` with the coordinator agent, shared trace, and metrics

Closing the app closes the ADK runner. It does **not** currently close the
shared SQLite connection or the process-global GitHub HTTP client.

## Agent graph

Root agent: **Coordinator** (`gemini-2.5-flash`)

Sub-agents:

- **GitHub agent** — repository questions via read-only tools
- **Security agent** — security explanation / memory tools
- **General agent** — general assistant + user memory tools

The GitHub agent may also use an advisory **security review** `AgentTool`. That
LLM review does not replace Guard.

All primary agents register `before_tool_callback` / `after_tool_callback`.

## Sessions

Two related but distinct session concepts:

1. **Orion `SessionInfo`** — title, user id, timestamps, message count (in-memory)
2. **ADK Session** — tool/state storage used during execution (in-memory by default)

The adapter maps Orion session UUIDs onto ADK sessions. Deleting one does not
automatically delete the other.

Conversation history is **not** restored across process restarts.

## Message execution

`AgentRunner.run_message`:

1. Records request-start metrics / traces
2. Ensures an ADK session exists
3. Sends user content through ADK
4. Collects events and keeps final-response text
5. Records success duration or failure metrics
6. Wraps unexpected failures as `OrionRuntimeError`

The runner can stream events, but the CLI buffers and prints final text only.

## Model configuration

The model name (`gemini-2.5-flash`) is hard-coded on agent definitions in v1.0.
It is not yet a typed config setting.

## Related docs

- [Architecture](architecture.md)
- [GitHub assistant guide](../guides/github-assistant.md)
- [Extending Orion](../development/extending-orion.md)
