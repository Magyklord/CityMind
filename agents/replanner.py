from agents.llm_client import ask_llm
from core.state import get_city_state
from core.metrics import increment


def create_replan(previous_decision):

    increment("replanning_events")
    state = get_city_state()

    prompt = f"""
You are the Replanning Agent in CityMind.

A previous city decision was made, but the situation may have
changed.

CURRENT CITY STATE:

Weather: {state["weather"]}
Temperature: {state["temperature"]}°C

Traffic level: {state["traffic_level"]}%
Blocked roads: {state["blocked_roads"]}

Emergency active: {state["emergency_incident"]}
Incident type: {state["incident_type"]}
Incident location: {state["incident_location"]}

PREVIOUS DECISION:

{previous_decision}

Determine whether the previous plan should remain active
or whether the city response should be changed.

Return ONLY valid JSON:

{{
    "replan_required": true,
    "reason": "Short explanation",
    "new_priority": "Short description of the new priority"
}}

Set replan_required to false if the previous plan is still
appropriate.

Do not include markdown.
Do not include any other text.
"""

    response = ask_llm(prompt)

    import json

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "replan_required": False,
            "reason": "Could not parse replanning response.",
            "new_priority": "Maintain previous plan."
        }