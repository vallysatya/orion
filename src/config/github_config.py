"""GitHub integration configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubConfig:
    """Settings for GitHub API access."""

    api_base_url: str = "https://api.github.com"
    token: str | None = None

    def __repr__(self) -> str:
        token_display = "***" if self.token else None
        return (
            f"GitHubConfig(api_base_url={self.api_base_url!r}, "
            f"token={token_display!r})"
        )
