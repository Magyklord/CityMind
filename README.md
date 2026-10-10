# CityMind — Agentic AI Smart City Operations

CityMind is an Agentic AI-based smart city decision-support prototype. It uses specialized AI agents to analyze simulated traffic, weather, road-blockage, and emergency scenarios and generate a consolidated recommendation through a web dashboard.

## Features

- **Multi-agent system:** Traffic, Weather, and Emergency agents.
- **Custom Python orchestration:** A planner selects relevant agents, an orchestrator coordinates their execution, and a supervisor synthesizes their findings.
- **LLM integration:** Groq API with the `openai/gpt-oss-20b` model.
- **MCP integration:** Tools for road-status checks, alternative routes, and emergency response-time estimates.
- **A2A interface:** Demonstrates exposing the Traffic Agent as a separate service.
- **RAG:** Retrieves relevant passages from a local city knowledge file.
- **Replanning and approval checks:** Includes basic workflow reconsideration and rule-based approval logic.
- **Web dashboard:** FastAPI-based interface for submitting scenarios and viewing structured recommendations.
- **Metrics:** Tracks selected workflow activity.

## Architecture

1. The user submits a city scenario through the website.
2. The planner identifies relevant agents.
3. The orchestrator coordinates the agents and collects their reports.
4. The specialist agents analyze traffic, weather, and emergency conditions.
5. MCP tools provide predefined road, route, and response-time information.
6. RAG retrieves relevant information from the local knowledge base.
7. The supervisor combines the available findings into a recommendation.
8. Replanning and approval components perform their implemented checks.
9. The presentation formatter structures the results.
10. The dashboard displays the recommendation and supporting information.

The main workflow uses custom Python orchestration. MCP provides tool integration, while A2A is demonstrated through the Traffic Agent interface; the entire workflow does not use A2A for every agent interaction.

## Technology Stack

- Python
- FastAPI and Uvicorn
- Groq API
- GPT-OSS 20B
- MCP (Model Context Protocol)
- A2A (Agent-to-Agent)
- HTML, CSS, and JavaScript

## Project Structure

```text
CityMind/
├── agents/
│   ├── planner.py
│   ├── orchestrator.py
│   ├── traffic.py
│   ├── weather.py
│   ├── emergency.py
│   ├── supervisor.py
│   ├── replanner.py
│   ├── approval.py
│   ├── llm_client.py
│   ├── mcp_client.py
│   ├── rag.py
│   └── presentation_formatter.py
├── a2a_agents/
│   ├── traffic_server.py
│   └── traffic_executor.py
├── core/
│   ├── state.py
│   └── metrics.py
├── knowledge/
│   └── city_knowledge.txt
├── tools/
│   └── city_tools.py
├── api.py
├── citymind.py
├── mcp_server.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Requirements

- Python 3.10 or newer recommended.
- A Groq API key.
- Internet access for package installation and hosted LLM inference.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CityMind
```

Replace the repository URL with your actual GitHub URL.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the environment

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Add your own Groq API key to `.env`:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Never publish your real API key or commit the `.env` file.

### 5. Run the web application

Start the FastAPI development server:

```powershell
uvicorn api:app --reload
```

Open the dashboard in your browser:

**http://127.0.0.1:8000**

Press `Ctrl+C` in the terminal to stop the server.

### Terminal mode

The project also contains `citymind.py`, which serves as a terminal entry point:

```powershell
python citymind.py
```

## Example Use Case

Consider an emergency vehicle travelling to a hospital during heavy rain. The specialist agents analyze the supplied scenario, the tools provide available route information, and the supervisor combines the findings into a recommendation.

The dashboard presents the recommended action, route details, estimated response time, risk information, reasoning, and next steps where available.

The route data and response-time calculations in the current prototype are simulated or predefined. They are not live traffic measurements or validated emergency predictions.

## Limitations

- Uses simulated or predefined city data.
- Does not control real traffic signals or dispatch emergency services.
- Uses basic lexical matching for local knowledge retrieval.
- Approval checks use simple rule-based phrase detection.
- LLM-generated responses may contain errors.
- The presentation formatter adds another LLM request.
- The main workflow primarily uses direct Python orchestration, with A2A demonstrated through the Traffic Agent interface.

## Future Enhancements

- Integrate live traffic and weather APIs.
- Improve route optimization and knowledge retrieval.
- Add stronger approval, validation, and error-handling mechanisms.
- Expand A2A communication between independently deployed agents.
- Evaluate recommendation accuracy and system performance.

## Security

Keep API keys and other credentials out of source code and version control. If a key has been exposed publicly, revoke it and replace it.

## License

Add a license file if you intend to specify how others may use, modify, or distribute this project.