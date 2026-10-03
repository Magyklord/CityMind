from agents.planner import create_plan

from agents.traffic import traffic_agent
from agents.weather import weather_agent
from agents.emergency import emergency_agent

from core.state import get_city_state
from core.metrics import increment


def run_dynamic_agents():

    state = get_city_state()

    # Ask the planner which agents are needed
    plan = create_plan(state)

    selected_agents = plan["agents"]

    print("\n===== DYNAMIC PLAN =====")
    print("Selected agents:")

    for agent in selected_agents:
        print("-", agent)

    print("\nReason:")
    print(plan["reason"])

    # Record selected agents
    increment(
        "agents_selected",
        len(selected_agents)
    )

    reports = {}

    # Run only the agents selected by the planner
    if "Traffic Agent" in selected_agents:

        increment("agent_calls")

        reports["Traffic Agent"] = traffic_agent(state)

    if "Weather Agent" in selected_agents:

        increment("agent_calls")

        reports["Weather Agent"] = weather_agent(state)

    if "Emergency Agent" in selected_agents:

        increment("agent_calls")

        reports["Emergency Agent"] = emergency_agent(state)

    return reports