from google.adk.tools.tool_context import ToolContext

from container import container


def remember_repository(
    repository: str,
    tool_context: ToolContext,
) -> dict:
    """
    Remember the GitHub repository currently being used.

    Args:
        repository: Repository name, such as "orion-guard".
    """
    cleaned_repository = repository.strip()

    if not cleaned_repository:
        return {
            "status": "error",
            "message": "Repository name cannot be empty.",
        }

    container.memory_service.set_current_repository(
        tool_context,
        cleaned_repository,
    )

    return {
        "status": "success",
        "current_repository": cleaned_repository,
    }


def get_current_repository(
    tool_context: ToolContext,
) -> dict:
    """Return the repository currently remembered for this session."""
    repository = container.memory_service.get_current_repository(
        tool_context,
    )

    if repository is None:
        return {
            "status": "not_found",
            "message": "No repository is currently selected.",
        }

    return {
        "status": "success",
        "current_repository": repository,
    }
