# Demo: inspect open GitHub issues

## Goal

Show the complete allowed path from a user request to a real, read-only GitHub
API call, including Guard, memory, and observability.

## Prerequisites

```bash
pip install -e ".[dev]"
```

Set `GOOGLE_API_KEY` in `.env`. A `GITHUB_TOKEN` is optional for public
repositories but recommended for authenticated rate limits.

## User request

```text
List the open issues in vallysatya/orion and summarize the most important ones.
```

Run it:

```bash
orion run "List the open issues in vallysatya/orion and summarize the most important ones."
```

## What Orion does internally

```text
User request
  → AgentRunner records RequestStarted / requests_total
  → Coordinator routes repository work to GitHubAgent
  → GitHubAgent proposes list_open_issues(owner="vallysatya", repo="orion")
  → before_tool_callback reads environment from MemoryService
  → GuardService evaluates six policies in order
  → no policy matches, so default_policy returns ALLOW
  → callback records last tool / security decision / risk score in session memory
  → list_open_issues calls GitHubClient
  → GitHubClient GETs /repos/vallysatya/orion/issues
  → GitHub request trace + counters + duration are recorded
  → after_tool_callback records successful tool execution + duration
  → GitHubAgent summarizes the returned issue data
  → AgentRunner records request success + duration
```

The flow is **Memory → Guard → Tool** at the callback boundary because Orion
first reads the remembered environment. Guard is still the mandatory gate
before the GitHub tool executes.

## Expected output

The exact issue titles and wording are live and model-dependent. Expect a
human-readable list or summary similar to:

```text
Open issues include:
- #<number> <current issue title> — <short summary>
- #<number> <current issue title> — <short summary>
```

If the repository has no open issues, the correct answer is an empty/no-open-
issues summary. If authentication or networking fails, expect a typed
`GitHubIntegrationError`, not a leaked `httpx` exception.

## Why this behavior is correct

- Reading issues is non-destructive, so Guard allows it.
- The tool uses the real GitHub client rather than invented model knowledge.
- Repository context remains session-local unless explicitly saved as a
  persistent preference.
- Tracing and metrics cover request, Guard, tool, and HTTP boundaries.
- Output is not hard-coded because live repository state changes.

## Verify the safety baseline

```bash
orion guard test
```

See also: [GitHub assistant guide](../docs/guides/github-assistant.md).
