import uvicorn

from starlette.applications import Starlette

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes
)
from a2a.server.tasks import InMemoryTaskStore

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill
)

from a2a_agents.traffic_executor import TrafficAgentExecutor


traffic_skill = AgentSkill(
    id="traffic_analysis",
    name="Traffic Analysis",
    description=(
        "Analyzes city traffic and emergency "
        "transportation impact."
    ),
    tags=[
        "traffic",
        "congestion",
        "roads",
        "emergency"
    ],
    examples=[
        "Analyze the current traffic situation.",
        "Determine whether emergency vehicles are affected."
    ],
    input_modes=["text/plain"],
    output_modes=["text/plain"]
)


agent_card = AgentCard(
    name="CityMind Traffic Agent",
    description=(
        "Traffic specialist agent for CityMind AI."
    ),
    version="1.0.0",

    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],

    capabilities=AgentCapabilities(
        streaming=False
    ),

    supported_interfaces=[
        AgentInterface(
            protocol_binding="JSONRPC",
            protocol_version="1.0",
            url="http://127.0.0.1:9999/"
        )
    ],

    skills=[
        traffic_skill
    ]
)


request_handler = DefaultRequestHandler(
    agent_executor=TrafficAgentExecutor(),
    task_store=InMemoryTaskStore(),
    agent_card=agent_card
)


routes = []

routes.extend(
    create_agent_card_routes(agent_card)
)

routes.extend(
    create_jsonrpc_routes(
        request_handler,
        rpc_url="/"
    )
)


app = Starlette(
    routes=routes
)


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=9999
    )