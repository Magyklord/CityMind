import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)

from core.metrics import increment


async def call_mcp_tools():

    server = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            road = await session.call_tool(
                "check_road_status",
                {
                    "road": "Road A"
                }
            )

            increment("mcp_calls")

            routes = await session.call_tool(
                "find_alternate_route",
                {
                    "start": "City Center",
                    "destination": "Hospital"
                }
            )

            increment("mcp_calls")

            response = await session.call_tool(
                "estimate_emergency_response",
                {
                    "incident_type": "accident",
                    "traffic_level": 75
                }
            )

            increment("mcp_calls")

            return {
                "road_status": road.content,
                "alternate_routes": routes.content,
                "emergency_response": response.content
            }


def get_city_tools():

    return asyncio.run(
        call_mcp_tools()
    )