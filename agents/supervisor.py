from agents.llm_client import ask_llm
from agents.mcp_client import get_city_tools
from agents.rag import retrieve_knowledge

from core.state import get_city_state, add_decision


def run_supervisor():

    state = get_city_state()

    # ------------------------------------------------
    # MCP: Get live city operational data
    # ------------------------------------------------

    mcp_data = get_city_tools()


    # ------------------------------------------------
    # RAG: Retrieve relevant city knowledge
    # ------------------------------------------------

    query = f"""
    {state["incident_type"]}
    {state["incident_location"]}
    {state["weather"]}
    {state["traffic_level"]}% traffic
    blocked roads
    emergency response
    alternate routes
    """

    knowledge = retrieve_knowledge(query)


    # ------------------------------------------------
    # Build supervisor prompt
    # ------------------------------------------------

    prompt = f"""
You are the City Supervisor in CityMind AI.

You coordinate specialist agents and make the final
city-level operational decision.

SPECIALIST AGENT REPORTS
------------------------

TRAFFIC AGENT:
{state["agent_reports"].get("Traffic Agent", "No report")}

WEATHER AGENT:
{state["agent_reports"].get("Weather Agent", "No report")}

EMERGENCY AGENT:
{state["agent_reports"].get("Emergency Agent", "No report")}


CURRENT CITY STATE
------------------

Weather: {state["weather"]}
Temperature: {state["temperature"]}°C

Traffic level: {state["traffic_level"]}%
Blocked roads: {state["blocked_roads"]}

Emergency active: {state["emergency_incident"]}
Incident type: {state["incident_type"]}
Incident location: {state["incident_location"]}


MCP OPERATIONAL DATA
--------------------

Road status:
{mcp_data["road_status"]}

Alternate routes:
{mcp_data["alternate_routes"]}

Emergency response estimate:
{mcp_data["emergency_response"]}


RETRIEVED CITY KNOWLEDGE
------------------------

{knowledge}


DECISION TASK
-------------

Use all of the information above to make a city-level
operational decision.

Your response must contain:

1. Overall situation
2. Most important risks
3. Immediate actions
4. Priority of each action
5. Recommended emergency route
6. Reason for the recommended route

Important rules:

- Use the MCP operational data when selecting routes.
- Use the retrieved city knowledge when determining risks
  and recommended actions.
- Do not invent roads, routes, incidents, or information.
- Do not claim that an action has already been executed.
- Clearly distinguish recommendations from completed actions.
"""

    decision = ask_llm(prompt)

    add_decision(decision)

    return decision