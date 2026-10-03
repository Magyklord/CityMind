# CityMind AI

## Agentic AI-Based Multi-Agent Framework for Autonomous Smart City Operations

CityMind is an agentic AI system that uses multiple specialized AI agents to analyze smart-city situations and coordinate operational decisions.

The system combines **multi-agent AI, Agent-to-Agent (A2A) communication, Model Context Protocol (MCP), Retrieval-Augmented Generation (RAG), dynamic agent selection, dynamic replanning, and human-in-the-loop approval**.

---

## Features

* **Multi-Agent System**

  * Traffic Agent
  * Weather Agent
  * Emergency Agent
  * City Supervisor

* **Dynamic Agent Selection**

  * A planning agent determines which specialist agents are relevant to the current situation.

* **A2A Communication**

  * Enables communication between agents using the Agent-to-Agent protocol.

* **MCP Integration**

  * Provides operational tools for:

    * Road status
    * Alternate route selection
    * Emergency response estimation

* **RAG**

  * Retrieves relevant information from a city knowledge base before the supervisor makes a decision.

* **Dynamic Replanning**

  * Evaluates whether an existing response should be changed when the situation changes.

* **Human-in-the-Loop**

  * High-risk actions can require human approval before proceeding.

* **System Metrics**

  * Tracks:

    * Selected agents
    * Agent calls
    * MCP tool calls
    * Replanning events
    * Approval events
    * Runtime

---

## System Architecture

```text
                         USER
                           │
                           ▼
                    CITYMIND SYSTEM
                           │
                           ▼
                       PLANNER
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        TRAFFIC         WEATHER       EMERGENCY
         AGENT            AGENT          AGENT
             │             │             │
             └─────────────┼─────────────┘
                           │
                          A2A
                           │
                           ▼
                     CITY SUPERVISOR
                       │         │
                       │         │
                      MCP       RAG
                       │         │
                       └────┬────┘
                            │
                            ▼
                    FINAL DECISION
                            │
                            ▼
                   HUMAN APPROVAL
                            │
                            ▼
                       ACTION / END
```

---

## Technologies Used

* Python
* Groq API
* A2A SDK
* Model Context Protocol (MCP)
* Retrieval-Augmented Generation (RAG)
* JSON-based agent communication
* Local knowledge base

---

## Project Structure

```text
CityMind_v2/
│
├── a2a_agents/
│   ├── __init__.py
│   ├── traffic_executor.py
│   └── traffic_server.py
│
├── agents/
│   ├── __init__.py
│   ├── approval.py
│   ├── emergency.py
│   ├── llm_client.py
│   ├── mcp_client.py
│   ├── orchestrator.py
│   ├── planner.py
│   ├── rag.py
│   ├── replanner.py
│   ├── supervisor.py
│   ├── traffic.py
│   └── weather.py
│
├── core/
│   ├── __init__.py
│   ├── metrics.py
│   └── state.py
│
├── knowledge/
│   └── city_knowledge.txt
│
├── tools/
│   ├── __init__.py
│   └── city_tools.py
│
├── citymind.py
├── mcp_server.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CityMind.git
cd CityMind
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit the `.env` file.

---

## Running CityMind

Run:

```powershell
python citymind.py
```

The system will ask for the current city scenario.

Example:

```text
===== CITYMIND SCENARIO =====

City [Chennai]: Chennai
State [Tamil Nadu]: Tamil Nadu
Weather [Heavy rain]: Heavy rain
Temperature (°C) [24]: 24
Traffic level (%) [75]: 85
Blocked road [Road A]: Road A
Emergency active? [Y/n]: y
Incident type [accident]: accident
Incident location [Road A]: Anna Salai
```

CityMind then:

1. Updates the current city state.
2. Determines which specialist agents are required.
3. Executes the selected agents.
4. Uses MCP tools for operational information.
5. Retrieves relevant information from the RAG knowledge base.
6. Generates a supervisor decision.
7. Checks whether human approval is required.
8. Displays system metrics.

---

## Example Workflow

```text
User Scenario
      │
      ▼
Dynamic Planner
      │
      ▼
Selected Specialist Agents
      │
      ├── Traffic Agent
      ├── Weather Agent
      └── Emergency Agent
      │
      ▼
MCP Operational Tools
      │
      ▼
RAG Knowledge Retrieval
      │
      ▼
City Supervisor
      │
      ▼
Risk Assessment
      │
      ▼
Human Approval
      │
      ▼
Final Decision
```

---

## Human-in-the-Loop

CityMind identifies potentially high-risk actions.

Examples include:

* Road closure
* Traffic rerouting
* Evacuation
* System shutdown

When such an action is proposed, the system requests human approval before proceeding.

---

## Evaluation Metrics

CityMind records basic runtime and system metrics including:

* Number of selected agents
* Number of agent calls
* Number of MCP tool calls
* Number of replanning events
* Number of approval requests
* Number of approvals
* Number of rejections
* Total execution time

These metrics can be used to evaluate the behavior and performance of the multi-agent system.

---

## Project Goal

The goal of CityMind is to demonstrate how agentic AI can coordinate multiple specialized agents and external tools to reason about dynamic smart-city situations.

The project focuses on **agent coordination and autonomous decision support**, while keeping high-risk operational actions subject to human approval.

---

## License

This project was developed as an academic project.
