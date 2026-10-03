from agents.llm_client import ask_llm
from core.state import save_agent_report


def traffic_agent(state):

    prompt = f"""
You are the Traffic Agent in CityMind AI.

Analyze the current city traffic situation.

Traffic level: {state["traffic_level"]}%
Blocked roads: {state["blocked_roads"]}
Accident: {state["accident"]}

Determine:

1. Traffic severity
2. Affected roads
3. Impact on emergency vehicles
4. Recommended traffic action

Give a concise report for the City Supervisor.
"""

    analysis = ask_llm(prompt)

    save_agent_report(
        "Traffic Agent",
        analysis
    )

    return analysis