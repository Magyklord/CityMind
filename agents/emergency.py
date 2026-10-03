from agents.llm_client import ask_llm
from core.state import save_agent_report


def emergency_agent(state):

    prompt = f"""
You are the Emergency Agent in CityMind AI.

Analyze the current emergency situation.

Emergency active: {state["emergency_incident"]}
Incident type: {state["incident_type"]}
Incident location: {state["incident_location"]}

Traffic level: {state["traffic_level"]}%
Blocked roads: {state["blocked_roads"]}

Determine:

1. Emergency severity
2. Response difficulties
3. Impact of traffic and blocked roads
4. Recommended emergency action

Give a concise report for the City Supervisor.
"""

    analysis = ask_llm(prompt)

    save_agent_report(
        "Emergency Agent",
        analysis
    )

    return analysis