from google.adk.agents import Agent

from callbacks.tool_callback import after_tool_callback, before_tool_callback
from tools.user_memory_tools import (
    get_user_name,
    get_user_preferences,
    remember_explanation_style,
    remember_preferred_language,
    remember_user_name,
)


general_agent = Agent(
    name="general_agent",
    model="gemini-2.5-flash",
    description=(
        "Handles general questions that are unrelated to GitHub "
        "operations or Orion Guard security."
    ),
    instruction="""
You are Orion's general assistant.

Answer ordinary questions clearly and helpfully.

When the user explicitly states their name, preferred language or
preferred explanation style, use the appropriate memory tool.

Use get_user_preferences when earlier preferences are relevant to the
current response.

Do not store sensitive information or infer preferences the user did not
explicitly provide.

Do not perform GitHub operations.
Do not make Orion Guard policy decisions.
Transfer specialized GitHub or security work to the appropriate agent.
""",
    tools=[
        remember_user_name,
        get_user_name,
        remember_preferred_language,
        remember_explanation_style,
        get_user_preferences,
    ],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
