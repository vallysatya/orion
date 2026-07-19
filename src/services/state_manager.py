"""
State Manager for Orion.

Responsible for updating and reading the structured
ConversationState during a conversation.
"""

from __future__ import annotations

from models.conversation_state import ConversationState


class StateManager:
    """
    Centralized manager for ConversationState.

    Tools should use this class instead of modifying
    ConversationState directly.
    """

    def __init__(self, state: ConversationState) -> None:
        self._state = state

    # ==========================================================
    # Generic Operations
    # ==========================================================

    def set(self, key: str, value) -> None:
        """Store a generic value."""
        self._state.set(key, value)

    def get(self, key: str, default=None):
        """Retrieve a generic value."""
        return self._state.get(key, default)

    def clear(self) -> None:
        """Clear the entire conversation state."""
        self._state.clear()

    # ==========================================================
    # Repository Context
    # ==========================================================

    def update_repository(self, repository: dict) -> None:
        """
        Store repository information.

        Expected GitHub response fields:
        owner.login
        name
        full_name
        language
        description
        stargazers_count
        forks_count
        open_issues_count
        default_branch
        html_url
        """

        owner = repository.get("owner", {}).get("login")

        self._state.set("repository", repository.get("full_name"))
        self._state.set("owner", owner)
        self._state.set("repo_name", repository.get("name"))
        self._state.set("language", repository.get("language"))
        self._state.set("description", repository.get("description"))
        self._state.set("stars", repository.get("stargazers_count"))
        self._state.set("forks", repository.get("forks_count"))
        self._state.set("open_issues", repository.get("open_issues_count"))
        self._state.set("default_branch", repository.get("default_branch"))
        self._state.set("repository_url", repository.get("html_url"))

        self._state.last_tool = "get_repository_info"
        self._state.last_agent = "github_agent"

    # ==========================================================
    # Issue Context
    # ==========================================================

    def update_issue(self, issue: dict) -> None:
        """Store selected issue information."""

        self._state.set("issue_number", issue.get("number"))
        self._state.set("issue_title", issue.get("title"))
        self._state.set("issue_state", issue.get("state"))
        self._state.set("issue_url", issue.get("html_url"))

        self._state.last_tool = "list_open_issues"
        self._state.last_agent = "github_agent"

    # ==========================================================
    # Pull Request Context
    # ==========================================================

    def update_pull_request(self, pull_request: dict) -> None:
        """Store selected pull request information."""

        self._state.set("pr_number", pull_request.get("number"))
        self._state.set("pr_title", pull_request.get("title"))
        self._state.set("pr_state", pull_request.get("state"))
        self._state.set("pr_url", pull_request.get("html_url"))

        self._state.last_tool = "list_pull_requests"
        self._state.last_agent = "github_agent"

    # ==========================================================
    # Conversation Helpers
    # ==========================================================

    def set_current_task(self, task: str) -> None:
        """Update the current task being performed."""
        self._state.current_task = task

    def set_last_tool(self, tool_name: str) -> None:
        """Record the last tool executed."""
        self._state.last_tool = tool_name

    def set_last_agent(self, agent_name: str) -> None:
        """Record the last agent that handled the request."""
        self._state.last_agent = agent_name

    # ==========================================================
    # Reset Methods
    # ==========================================================

    def clear_repository(self) -> None:
        """Remove repository-related context."""

        repository_keys = [
            "repository",
            "owner",
            "repo_name",
            "language",
            "description",
            "stars",
            "forks",
            "open_issues",
            "default_branch",
            "repository_url",
        ]

        for key in repository_keys:
            self._state.remove(key)

    def clear_issue(self) -> None:
        """Remove issue-related context."""

        issue_keys = [
            "issue_number",
            "issue_title",
            "issue_state",
            "issue_url",
        ]

        for key in issue_keys:
            self._state.remove(key)

    def clear_pull_request(self) -> None:
        """Remove pull request-related context."""

        pr_keys = [
            "pr_number",
            "pr_title",
            "pr_state",
            "pr_url",
        ]

        for key in pr_keys:
            self._state.remove(key)