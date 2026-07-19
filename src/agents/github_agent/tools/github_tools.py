"""
GitHub tools exposed to the Google ADK agent.

This module contains thin wrappers around GitHubClient methods.
The agent invokes these tools, while GitHubClient handles all
HTTP communication with the GitHub REST API.
"""

from __future__ import annotations

from agents.github_agent.clients.github_client import GitHubClient

# Singleton client shared across all tool invocations.
github_client = GitHubClient()


def get_repository_info(owner: str, repo: str) -> dict:
    """
    Retrieve metadata about a GitHub repository.

    Args:
        owner: Repository owner (e.g. "google")
        repo: Repository name (e.g. "adk-python")

    Returns:
        Repository metadata.
    """
    return github_client.get_repository(owner, repo)


def list_my_repositories(limit: int = 30) -> list[dict]:
    """
    List repositories for the authenticated GitHub account.

    Args:
        limit: Maximum number of repositories to return.

    Returns:
        Repositories owned by or accessible to the authenticated user.
    """
    return github_client.list_my_repositories(limit)


def search_repositories(query: str, limit: int = 5) -> list[dict]:
    """
    Search GitHub repositories.

    Args:
        query: Search keyword.
        limit: Maximum number of repositories.

    Returns:
        Matching repositories.
    """
    return github_client.search_repositories(query, limit)


def list_open_issues(owner: str, repo: str) -> list[dict]:
    """
    List open issues for a repository.
    """
    return github_client.get_open_issues(owner, repo)


def list_pull_requests(owner: str, repo: str) -> list[dict]:
    """
    List open pull requests.
    """
    return github_client.get_pull_requests(owner, repo)


def get_latest_release(owner: str, repo: str) -> dict:
    """
    Retrieve the latest repository release.
    """
    return github_client.get_latest_release(owner, repo)


def list_contributors(owner: str, repo: str) -> list[dict]:
    """
    List repository contributors.
    """
    return github_client.get_contributors(owner, repo)


def get_recent_commits(owner: str, repo: str) -> list[dict]:
    """
    Retrieve recent commits.
    """
    return github_client.get_recent_commits(owner, repo)


def get_repository_languages(owner: str, repo: str) -> dict:
    """
    Retrieve repository languages.
    """
    return github_client.get_languages(owner, repo)


def get_repository_topics(owner: str, repo: str) -> list[str]:
    """
    Retrieve repository topics.
    """
    return github_client.get_topics(owner, repo)


def get_repository_license(owner: str, repo: str) -> dict:
    """
    Retrieve repository license information.
    """
    return github_client.get_license(owner, repo)