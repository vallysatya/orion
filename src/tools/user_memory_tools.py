from google.adk.tools.tool_context import ToolContext

from container import container


def remember_user_name(
    name: str,
    tool_context: ToolContext,
) -> dict:
    """Remember the user's preferred name for the current session."""
    cleaned_name = name.strip()

    if not cleaned_name:
        return {
            "status": "error",
            "message": "Name cannot be empty.",
        }

    container.memory_service.set_user_name(
        tool_context,
        cleaned_name,
    )

    return {
        "status": "success",
        "user_name": cleaned_name,
    }


def get_user_name(
    tool_context: ToolContext,
) -> dict:
    """Return the user's remembered name."""
    name = container.memory_service.get_user_name(tool_context)

    if name is None:
        return {
            "status": "not_found",
            "message": "No user name has been remembered.",
        }

    return {
        "status": "success",
        "user_name": name,
    }


def remember_preferred_language(
    language: str,
    tool_context: ToolContext,
) -> dict:
    """Remember the user's preferred response language."""
    cleaned_language = language.strip()

    if not cleaned_language:
        return {
            "status": "error",
            "message": "Language cannot be empty.",
        }

    container.memory_service.set_preferred_language(
        tool_context,
        cleaned_language,
    )

    return {
        "status": "success",
        "preferred_language": cleaned_language,
    }


def remember_explanation_style(
    style: str,
    tool_context: ToolContext,
) -> dict:
    """
    Remember the user's preferred explanation style.

    Examples: simple, concise, detailed, beginner-friendly.
    """
    cleaned_style = style.strip().lower()

    if not cleaned_style:
        return {
            "status": "error",
            "message": "Explanation style cannot be empty.",
        }

    container.memory_service.set_explanation_style(
        tool_context,
        cleaned_style,
    )

    return {
        "status": "success",
        "explanation_style": cleaned_style,
    }


def get_user_preferences(
    tool_context: ToolContext,
) -> dict:
    """Return all remembered user preferences."""
    return {
        "status": "success",
        "user_name": container.memory_service.get_user_name(
            tool_context,
        ),
        "preferred_language": (
            container.memory_service.get_preferred_language(
                tool_context,
            )
        ),
        "explanation_style": (
            container.memory_service.get_explanation_style(
                tool_context,
            )
        ),
    }
