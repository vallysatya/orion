"""
GitHub AI Assistant Agent.

Creates and configures the Google ADK Agent.
"""

from google.adk.agents import Agent

from agents.github_agent.prompt import GITHUB_AGENT_PROMPT
from agents.github_agent.tools.github_tools import (
    get_latest_release,
    get_recent_commits,
    get_repository_info,
    get_repository_languages,
    get_repository_license,
    get_repository_topics,
    list_contributors,
    list_open_issues,
    list_pull_requests,
    search_repositories,
)

github_agent = Agent(
    name="github_assistant",
    model="gemini-2.5-flash",
    description=(
        "An AI assistant capable of exploring GitHub repositories "
        "using real GitHub API tools."
    ),
    instruction=GITHUB_AGENT_PROMPT,
    tools=[
        get_repository_info,
        search_repositories,
        list_open_issues,
        list_pull_requests,
        get_latest_release,
        list_contributors,
        get_recent_commits,
        get_repository_languages,
        get_repository_topics,
        get_repository_license,
    ],
)
