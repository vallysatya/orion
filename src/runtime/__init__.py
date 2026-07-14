"""ADK runtime package.

Uses Google ADK 2.4 public APIs:
- App
- InMemoryRunner
- session_service.create_session
- run_async + google.genai.types.Content
"""

from runtime.app import create_app
from runtime.runner import AgentRunner

__all__ = ["AgentRunner", "create_app"]
