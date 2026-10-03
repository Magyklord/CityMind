from agents.llm_client import ask_llm
from core.state import save_agent_report


def weather_agent(state):

    prompt = f"""
You are the Weather Agent in CityMind AI.

Analyze the current weather conditions.

Weather: {state["weather"]}
Temperature: {state["temperature"]}°C

Determine:

1. Weather severity
2. Impact on city operations
3. Possible impact on emergency services
4. Recommended action

Give a concise report for the City Supervisor.
"""

    analysis = ask_llm(prompt)

    save_agent_report(
        "Weather Agent",
        analysis
    )

    return analysis