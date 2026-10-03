CITY_STATE = {
    "city": "Chennai",
    "state": "Tamil Nadu",

    "weather": "Heavy rain",
    "temperature": 24,

    "traffic_level": 75,
    "blocked_roads": ["Road A"],
    "accident": True,

    "emergency_incident": True,
    "incident_type": "accident",
    "incident_location": "Road A",

    "agent_reports": {},
    "decisions": []
}


def get_city_state():
    return CITY_STATE


def update_city_state(**updates):
    CITY_STATE.update(updates)


def save_agent_report(agent, report):
    CITY_STATE["agent_reports"][agent] = report


def add_decision(decision):
    CITY_STATE["decisions"].append(decision)