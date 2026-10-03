from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.helpers import new_text_message

from agents.traffic import traffic_agent
from core.state import get_city_state


class TrafficAgentExecutor(AgentExecutor):

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ):

        state = get_city_state()

        result = traffic_agent(state)

        await event_queue.enqueue_event(
            new_text_message(
                text=result
            )
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ):

        await event_queue.enqueue_event(
            new_text_message(
                text="Traffic analysis cancelled."
            )
        )