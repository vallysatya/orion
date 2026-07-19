from google.adk.agents import Agent

from agents.general_agent import general_agent
from agents.github_agent import github_agent
from agents.security_agent import security_agent
from callbacks.tool_callback import before_tool_callback
from tools.security_memory_tools import (
    get_environment,
    remember_environment,
)
from tools.user_memory_tools import (
    get_user_preferences,
    remember_explanation_style,
    remember_preferred_language,
    remember_user_name,
)


coordinator_agent = Agent(
    name="orion_coordinator",
    model="gemini-2.5-flash",
    description="Routes user requests to the correct Orion specialist.",
    instruction="""
You are the coordinator for Orion.

Your primary job is to understand the user's request and transfer it
to the most appropriate specialist agent.

Shared memory rules:

1. If the user sets a global environment, store it using
   remember_environment before routing later environment-dependent work.

2. If the user explicitly provides their name, preferred language or
   explanation style, store that information using the appropriate tool.

3. Route GitHub work to github_agent.

4. Route Orion Guard, policy, risk, approval and security questions to
   security_agent.

5. Route ordinary questions to general_agent.

6. Do not store secrets, access tokens, passwords, private keys or other
   sensitive credentials in session memory.

Do not perform specialist work yourself when a suitable sub-agent exists.
Do not invent the result of a tool execution.
""",
    tools=[
        remember_environment,
        get_environment,
        remember_user_name,
        remember_preferred_language,
        remember_explanation_style,
        get_user_preferences,
    ],
    sub_agents=[
        github_agent,
        security_agent,
        general_agent,
    ],
    before_tool_callback=before_tool_callback,
)
