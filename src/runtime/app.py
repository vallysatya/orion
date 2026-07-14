"""ADK App definition (ADK 2.4)."""

from __future__ import annotations

from google.adk.apps import App

from agents.github_agent.agent import github_agent
from config import APP_NAME


def create_app() -> App:
    """Build the Orion ADK application.

    The App is the top-level ADK container. It owns the root agent that
    InMemoryRunner / Runner execute.
    """
    return App(
        name=APP_NAME,
        root_agent=github_agent,
    )
