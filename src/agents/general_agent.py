from google.adk.agents import Agent


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

Do not perform GitHub operations.
Do not make Orion Guard policy decisions.
Transfer specialized GitHub or security work to the appropriate agent.
""",
)
