from mcp.server.fastmcp import FastMCP

from tools.city_tools import (
    road_status,
    alternate_route,
    emergency_response
)


mcp = FastMCP("CityMind City Operations")


@mcp.tool()
def check_road_status(road: str) -> dict:
    """Check whether a city road is open, blocked, or congested."""
    return road_status(road)


@mcp.tool()
def find_alternate_route(
    start: str,
    destination: str
) -> list:
    """Find alternative routes between two locations."""
    return alternate_route(start, destination)


@mcp.tool()
def estimate_emergency_response(
    incident_type: str,
    traffic_level: float
) -> dict:
    """Estimate emergency response time."""
    return emergency_response(
        incident_type,
        traffic_level
    )


if __name__ == "__main__":
    mcp.run()