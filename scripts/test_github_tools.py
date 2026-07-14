"""Smoke test GitHub agent tools."""

from __future__ import annotations

from agents.github_agent.tools.github_tools import (
    get_recent_commits,
    get_repository_info,
    get_repository_license,
    list_contributors,
    search_repositories,
)


def main() -> None:
    print("=== get_repository_info(vallysatya/orion) ===")
    info = get_repository_info("vallysatya", "orion")
    for key, value in info.items():
        print(f"  {key}: {value}")

    print()
    print('=== search_repositories("orion agent", limit=2) ===')
    for repo in search_repositories("orion agent", limit=2):
        print(f"  {repo['name']} stars={repo['stars']}")

    print()
    print("=== get_repository_license ===")
    print(" ", get_repository_license("vallysatya", "orion"))

    print()
    print("=== list_contributors ===")
    print(" ", list_contributors("vallysatya", "orion"))

    print()
    print("=== get_recent_commits ===")
    for commit in get_recent_commits("vallysatya", "orion")[:3]:
        print(f"  {commit['sha']} {commit['message']}")

    print()
    print("GitHub tools OK")


if __name__ == "__main__":
    main()
