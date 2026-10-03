import time

from agents.orchestrator import run_dynamic_agents
from agents.supervisor import run_supervisor
from agents.approval import requires_approval, request_approval

from core.state import get_city_state, update_city_state
from core.metrics import reset_metrics, get_metrics, increment, add_runtime


def ask(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def ask_num(prompt, default):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()

        if not value:
            return default

        try:
            return float(value)
        except ValueError:
            print("Enter a valid number.")


def ask_bool(prompt, default=True):
    suffix = "Y/n" if default else "y/N"

    while True:
        value = input(f"{prompt} [{suffix}]: ").strip().lower()

        if not value:
            return default

        if value in ("y", "yes"):
            return True

        if value in ("n", "no"):
            return False

        print("Enter yes or no.")


def get_scenario():

    print("\n===== CITYMIND SCENARIO =====")

    city = ask("City", "Chennai")
    state = ask("State", "Tamil Nadu")
    weather = ask("Weather", "Heavy rain")
    temperature = ask_num("Temperature (°C)", 24)
    traffic = ask_num("Traffic level (%)", 75)
    blocked = ask("Blocked road", "Road A")
    emergency = ask_bool("Emergency active?", True)
    incident = ask("Incident type", "accident")
    location = ask("Incident location", "Road A")

    blocked_roads = [] if blocked.lower() == "none" else [blocked]

    update_city_state(
        city=city,
        state=state,
        weather=weather,
        temperature=temperature,
        traffic_level=traffic,
        blocked_roads=blocked_roads,
        accident=emergency and incident.lower() == "accident",
        emergency_incident=emergency,
        incident_type=incident,
        incident_location=location,
        agent_reports={},
        decisions=[]
    )


def show_state():

    s = get_city_state()

    print("\n===== CITY SITUATION =====")
    print(f"City:          {s['city']}, {s['state']}")
    print(f"Weather:       {s['weather']}")
    print(f"Temperature:   {s['temperature']}°C")
    print(f"Traffic:       {s['traffic_level']}%")
    print(f"Blocked roads: {s['blocked_roads'] or 'None'}")
    print(f"Emergency:     {s['emergency_incident']}")
    print(f"Incident:      {s['incident_type']}")
    print(f"Location:      {s['incident_location']}")


def show_metrics():

    m = get_metrics()

    print("\n===== SYSTEM METRICS =====")
    print(f"Agents selected:   {m['agents_selected']}")
    print(f"Agent calls:       {m['agent_calls']}")
    print(f"MCP tool calls:    {m['mcp_calls']}")
    print(f"Replanning events: {m['replanning_events']}")
    print(f"Approval required: {m['approval_required']}")
    print(f"Approvals:         {m['approvals']}")
    print(f"Rejections:        {m['rejections']}")
    print(f"Runtime:           {m['total_runtime_seconds']:.2f}s")


def run_citymind():

    reset_metrics()
    start = time.time()
    increment("run_count")

    print("\n========================================")
    print("             CITYMIND AI")
    print("========================================")
    print("Agentic Smart City Operations System")

    get_scenario()
    show_state()

    print("\n===== DYNAMIC AGENT PLANNING =====")

    reports = run_dynamic_agents()

    print("\n===== AGENT REPORTS =====")

    for agent, report in reports.items():
        print(f"\n--- {agent} ---")
        print(report)

    print("\n===== CITY SUPERVISOR =====")

    decision = run_supervisor()

    print("\n--- FINAL DECISION ---")
    print(decision)

    if requires_approval(decision):

        print("\n===== HUMAN APPROVAL =====")

        if request_approval(decision):
            print("\nACTION APPROVED")
        else:
            print("\nACTION REJECTED")

    else:
        print("\n===== RISK CHECK =====")
        print("No human approval required.")

    add_runtime(time.time() - start)
    show_metrics()

    print("\n========================================")
    print("        CITYMIND RUN COMPLETE")
    print("========================================")


if __name__ == "__main__":
    run_citymind()