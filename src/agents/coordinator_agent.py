from google.adk.agents import Agent

from agents.general_agent import general_agent
from agents.github_agent import github_agent
from agents.security_agent import security_agent


coordinator_agent = Agent(
    name="orion_coordinator",
    model="gemini-2.5-flash",
    description="Routes user requests to the correct Orion specialist.",
    instruction="""
You are the coordinator for Orion.

Your primary job is to understand the user's request and transfer it
to the most appropriate specialist agent.

Routing rules:

1. Transfer GitHub repository, issue, branch and pull-request requests
   to github_agent.

2. Transfer questions about blocked actions, approvals, permissions,
   PII, prompt injection, policies and security decisions to
   security_agent.

3. Transfer other general questions to general_agent.

Do not perform specialist work yourself when a suitable sub-agent exists.
Do not invent the result of a tool execution.
""",
    sub_agents=[
        github_agent,
        security_agent,
        general_agent,
    ],
)
