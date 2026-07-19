"""
GitHub AI Assistant Agent.

Creates and configures the Google ADK Agent.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from agents.github_agent.prompt import GITHUB_AGENT_PROMPT
from agents.github_agent.tools.github_tools import (
    get_latest_release,
    get_recent_commits,
    get_repository_info,
    get_repository_languages,
    get_repository_license,
    get_repository_topics,
    list_contributors,
    list_my_repositories,
    list_open_issues,
    list_pull_requests,
    search_repositories,
)
from agents.security_review_agent import security_review_agent
from callbacks.tool_callback import before_tool_callback
from tools.repository_memory_tools import (
    get_current_repository,
    remember_repository,
)
from tools.security_memory_tools import (
    get_environment,
    get_user_role,
)

security_review_tool = AgentTool(
    agent=security_review_agent,
)

github_agent = Agent(
    name="github_agent",
    model="gemini-2.5-flash",
    description=(
        "Handles GitHub repository operations, issues, branches, "
        "pull requests and repository information."
    ),
    instruction=GITHUB_AGENT_PROMPT,
    tools=[
        remember_repository,
        get_current_repository,
        get_environment,
        get_user_role,
        security_review_tool,
        list_my_repositories,
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
    before_tool_callback=before_tool_callback,
)
