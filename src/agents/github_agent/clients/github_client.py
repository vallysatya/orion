"""
GitHub API client.

This module provides a reusable client for interacting with the GitHub REST API.
It is intentionally independent of Google ADK so it can be reused by any service.
"""

from __future__ import annotations

from typing import Any

import httpx

from config import GITHUB_API_BASE_URL, GITHUB_TOKEN


class GitHubClient:
    """Reusable GitHub REST API client."""

    def __init__(self) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

        self._client = httpx.Client(
            base_url=GITHUB_API_BASE_URL,
            timeout=30.0,
            headers=headers,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Send an HTTP request to GitHub.

        Raises:
            RuntimeError: if GitHub returns an error.
        """
        response = self._client.request(
            method=method,
            url=endpoint,
            params=params,
        )

        if response.status_code >= 400:
            raise RuntimeError(
                f"GitHub API Error {response.status_code}: {response.text}"
            )

        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    # ------------------------------------------------------------------
    # Repository
    # ------------------------------------------------------------------

    def get_repository(
        self,
        owner: str,
        repo: str,
    ) -> dict[str, Any]:
        """Return repository metadata."""
        data = self._request("GET", f"/repos/{owner}/{repo}")

        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "watchers": data["watchers_count"],
            "language": data["language"],
            "default_branch": data["default_branch"],
            "open_issues": data["open_issues_count"],
            "license": (
                data["license"]["name"]
                if data.get("license")
                else None
            ),
            "url": data["html_url"],
        }

    # ------------------------------------------------------------------
    # Authenticated user
    # ------------------------------------------------------------------

    def list_my_repositories(
        self,
        limit: int = 30,
    ) -> list[dict[str, Any]]:
        """List repositories for the authenticated GitHub user."""
        data = self._request(
            "GET",
            "/user/repos",
            params={
                "per_page": limit,
                "sort": "updated",
                "affiliation": "owner,collaborator,organization_member",
            },
        )

        return [
            {
                "name": repo["full_name"],
                "private": repo["private"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "description": repo["description"],
                "url": repo["html_url"],
                "updated_at": repo["updated_at"],
            }
            for repo in data
        ]

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search_repositories(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Search GitHub repositories."""
        data = self._request(
            "GET",
            "/search/repositories",
            params={
                "q": query,
                "per_page": limit,
            },
        )

        return [
            {
                "name": repo["full_name"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "description": repo["description"],
                "url": repo["html_url"],
            }
            for repo in data.get("items", [])
        ]

    # ------------------------------------------------------------------
    # Issues & pull requests
    # ------------------------------------------------------------------

    def get_open_issues(
        self,
        owner: str,
        repo: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """List open issues for a repository (excludes pull requests)."""
        data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/issues",
            params={"state": "open", "per_page": limit},
        )

        return [
            {
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "author": issue["user"]["login"] if issue.get("user") else None,
                "labels": [label["name"] for label in issue.get("labels", [])],
                "comments": issue.get("comments", 0),
                "created_at": issue["created_at"],
                "url": issue["html_url"],
            }
            for issue in data
            if "pull_request" not in issue
        ]

    def get_pull_requests(
        self,
        owner: str,
        repo: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """List open pull requests for a repository."""
        data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls",
            params={"state": "open", "per_page": limit},
        )

        return [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "author": pr["user"]["login"] if pr.get("user") else None,
                "head_branch": pr["head"]["ref"],
                "base_branch": pr["base"]["ref"],
                "created_at": pr["created_at"],
                "url": pr["html_url"],
            }
            for pr in data
        ]

    # ------------------------------------------------------------------
    # Releases & commits
    # ------------------------------------------------------------------

    def get_latest_release(
        self,
        owner: str,
        repo: str,
    ) -> dict[str, Any]:
        """Retrieve the latest repository release."""
        data = self._request("GET", f"/repos/{owner}/{repo}/releases/latest")

        return {
            "tag_name": data["tag_name"],
            "name": data.get("name"),
            "published_at": data["published_at"],
            "author": data["author"]["login"] if data.get("author") else None,
            "draft": data.get("draft", False),
            "prerelease": data.get("prerelease", False),
            "url": data["html_url"],
        }

    def get_recent_commits(
        self,
        owner: str,
        repo: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Retrieve recent commits on the default branch."""
        data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/commits",
            params={"per_page": limit},
        )

        return [
            {
                "sha": commit["sha"][:7],
                "message": commit["commit"]["message"].splitlines()[0],
                "author": commit["commit"]["author"]["name"]
                if commit["commit"].get("author")
                else None,
                "date": commit["commit"]["author"]["date"]
                if commit["commit"].get("author")
                else None,
                "url": commit["html_url"],
            }
            for commit in data
        ]

    # ------------------------------------------------------------------
    # Contributors & metadata
    # ------------------------------------------------------------------

    def get_contributors(
        self,
        owner: str,
        repo: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """List repository contributors."""
        data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/contributors",
            params={"per_page": limit},
        )

        return [
            {
                "username": contributor["login"],
                "contributions": contributor["contributions"],
                "profile_url": contributor["html_url"],
            }
            for contributor in data
        ]

    def get_languages(
        self,
        owner: str,
        repo: str,
    ) -> dict[str, int]:
        """Retrieve repository language breakdown (language -> bytes)."""
        data = self._request("GET", f"/repos/{owner}/{repo}/languages")
        return dict(data)

    def get_topics(
        self,
        owner: str,
        repo: str,
    ) -> list[str]:
        """Retrieve repository topics."""
        response = self._client.get(
            f"/repos/{owner}/{repo}/topics",
            headers={
                **self._client.headers,
                "Accept": "application/vnd.github.mercy-preview+json",
            },
        )

        if response.status_code >= 400:
            raise RuntimeError(
                f"GitHub API Error {response.status_code}: {response.text}"
            )

        data = response.json()
        return list(data.get("names", []))

    def get_license(
        self,
        owner: str,
        repo: str,
    ) -> dict[str, Any]:
        """Retrieve repository license information."""
        try:
            data = self._request("GET", f"/repos/{owner}/{repo}/license")
            return {
                "key": data["license"]["key"],
                "name": data["license"]["name"],
                "spdx_id": data["license"].get("spdx_id"),
                "url": data.get("html_url"),
            }
        except RuntimeError as exc:
            if "404" in str(exc):
                return {"name": None, "message": "No license detected for this repository."}
            raise

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
