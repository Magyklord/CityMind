def road_status(road):
    roads = {
        "Road A": {
            "status": "blocked",
            "reason": "Accident and heavy rain"
        },
        "Road B": {
            "status": "open",
            "reason": "Normal"
        },
        "Road C": {
            "status": "congested",
            "reason": "Heavy traffic"
        }
    }

    return roads.get(
        road,
        {
            "status": "unknown",
            "reason": "No information available"
        }
    )


def alternate_route(start, destination):
    return [
        {
            "route": f"{start} -> Road B -> {destination}",
            "estimated_time": 9,
            "risk": "Low"
        },
        {
            "route": f"{start} -> Road C -> {destination}",
            "estimated_time": 14,
            "risk": "Medium"
        }
    ]


def emergency_response(incident_type, traffic_level):
    base_times = {
        "medical": 7,
        "fire": 8,
        "accident": 10
    }

    base_time = base_times.get(incident_type, 10)

    if traffic_level > 80:
        multiplier = 2.0
    elif traffic_level > 60:
        multiplier = 1.5
    else:
        multiplier = 1.0

    return {
        "incident": incident_type,
        "estimated_response_time": round(
            base_time * multiplier,
            1
        ),
        "unit": "minutes"
    }