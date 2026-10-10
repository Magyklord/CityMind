
import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def format_citymind_results(scenario, reports, decision):
    """Format actual CityMind outputs for the website."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing from your local .env file."
        )

    system_prompt = """
You are CityMind's presentation formatter for a smart-city
decision-support prototype.

Format the supplied scenario, specialist-agent reports, and
supervisor decision as a professional dashboard report.

You are NOT the decision-maker.

STRICT RULES:
- Preserve the supervisor's decision and its meaning.
- Never invent facts, routes, timings, risk levels, or observations.
- Never claim that an action has been executed unless the source says so.
- Use null for unavailable route, response time, or risk information.
- Keep agent reports accurately attributed.
- Distinguish observations from recommendations.
- Return valid JSON only, without Markdown fences.

FORMATTING REQUIREMENTS:

1. headline:
   A short incident title, maximum 12 words.
   Never put the entire recommendation or numbered list here.

2. status:
   A short status label, such as "Analysis complete".

3. recommended_action:
   One concise summary sentence, maximum 35 words.
   Never put a numbered list or multiple separate actions here.

4. next_steps:
   Extract every distinct recommended action from the supervisor
   decision. Put each action in a separate string.
   Remove leading numbering from each action.
   Preserve useful explanations and do not combine unrelated actions.

5. reasoning:
   Return concise reasons supported by the supplied information.
   Do not repeat the entire action list.

6. route, response_time, risk_level:
   Populate only when supported by the scenario, reports, or decision.
   Otherwise return null.
   Never infer a low risk merely because no high risk was mentioned.

7. agent_cards:
   Return one card for every actual specialist report.
   Each card must contain name, summary, findings, and status.
   Do not invent reports for agents that did not run.

8. limitations:
   List relevant missing information and uncertainties.

Return this JSON structure:
{
  "headline": "Short incident title",
  "status": "Analysis complete",
  "recommended_action": "One concise summary sentence",
  "route": null,
  "response_time": null,
  "risk_level": null,
  "reasoning": [],
  "next_steps": [],
  "agent_cards": [
    {
      "name": "Agent name",
      "summary": "Concise accurate summary",
      "findings": [],
      "status": "Report received"
    }
  ],
  "limitations": []
}
"""

    payload = {
        "scenario": scenario,
        "agent_reports": reports,
        "supervisor_decision": decision,
    }

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(
                    payload,
                    ensure_ascii=False,
                    default=str,
                ),
            },
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
        max_completion_tokens=2200,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "The presentation formatter returned an empty response."
        )

    result = json.loads(content)

    required_fields = (
        "headline",
        "status",
        "recommended_action",
        "route",
        "response_time",
        "risk_level",
        "reasoning",
        "next_steps",
        "agent_cards",
        "limitations",
    )

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Formatter response is missing '{field}'."
            )

    for field in (
        "reasoning",
        "next_steps",
        "agent_cards",
        "limitations",
    ):
        if not isinstance(result[field], list):
            raise ValueError(
                f"Formatter field '{field}' must be a list."
            )

    return result
