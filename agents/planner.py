import json

from agents.llm_client import ask_llm


def create_plan(state):

    prompt = f"""
You are the planning agent for CityMind, an autonomous
smart-city multi-agent system.

Analyze the current city situation and decide which specialist
agents should be consulted.

Available agents:

1. Traffic Agent
   - analyzes traffic
   - blocked roads
   - congestion
   - transportation impact

2. Weather Agent
   - analyzes weather
   - rain
   - temperature
   - weather-related operational risks

3. Emergency Agent
   - analyzes accidents
   - emergency incidents
   - emergency response difficulties

CURRENT CITY STATE:

Weather: {state["weather"]}
Temperature: {state["temperature"]}°C

Traffic level: {state["traffic_level"]}%
Blocked roads: {state["blocked_roads"]}

Emergency active: {state["emergency_incident"]}
Incident type: {state["incident_type"]}
Incident location: {state["incident_location"]}

Choose only the agents that are relevant.

Return ONLY valid JSON in this exact format:

{{
    "agents": [
        "Traffic Agent",
        "Weather Agent"
    ],
    "reason": "Short explanation"
}}

Do not include markdown.
Do not include any other text.
"""

    response = ask_llm(prompt)

    try:
        plan = json.loads(response)
    except json.JSONDecodeError:

        plan = {
            "agents": [
                "Traffic Agent",
                "Weather Agent",
                "Emergency Agent"
            ],
            "reason": "Planner response could not be parsed."
        }

    return plan