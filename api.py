
import time
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from agents.orchestrator import run_dynamic_agents
from agents.supervisor import run_supervisor
from agents.approval import requires_approval
from agents.presentation_formatter import format_citymind_results
from core.state import CITY_STATE
from core.metrics import METRICS


app = FastAPI(title="CityMind Operations Center")
run_lock = Lock()


class CityScenario(BaseModel):
    city: str = "Chennai"
    state: str = "Tamil Nadu"
    temperature: float = 24
    weather: str = "Heavy rain"
    traffic_level: int = Field(default=75, ge=0, le=100)
    blocked_roads: list[str] = Field(
        default_factory=lambda: ["Road A"]
    )
    accident: bool = True
    emergency_incident: bool = True
    incident_type: str = "accident"
    incident_location: str = "Road A"


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML


@app.get("/api/metrics")
def get_metrics():
    return dict(METRICS)


@app.post("/api/run")
def run_citymind(scenario: CityScenario):
    with run_lock:
        started = time.perf_counter()

        try:
            values = scenario.model_dump()

            # Update the existing shared city state.
            CITY_STATE.update(values)
            CITY_STATE["agent_reports"] = {}
            CITY_STATE["decisions"] = []

            # Execute the existing CityMind workflow.
            reports = run_dynamic_agents() or {}
            CITY_STATE["agent_reports"] = reports

            decision = run_supervisor()

            decision_text = (
                decision
                if isinstance(decision, str)
                else str(decision)
            )

            CITY_STATE["decisions"].append(decision_text)

            approval_needed = requires_approval(decision_text)

            # Second Groq call: format the real outputs for the UI.
            presentation = format_citymind_results(
                scenario=values,
                reports=reports,
                decision=decision_text,
            )

            # Update the existing metrics.
            METRICS["run_count"] = (
                METRICS.get("run_count", 0) + 1
            )

            METRICS["agent_calls"] = (
                METRICS.get("agent_calls", 0) + len(reports)
            )

            if approval_needed:
                METRICS["approval_required"] = (
                    METRICS.get("approval_required", 0) + 1
                )

            elapsed = time.perf_counter() - started

            METRICS["total_runtime_seconds"] = (
                METRICS.get("total_runtime_seconds", 0)
                + elapsed
            )

            return {
                "presentation": presentation,
                "approval_required": approval_needed,
                "metrics": dict(METRICS),
                "technical": {
                    "supervisor_decision": decision_text,
                    "agent_reports": reports,
                },
            }

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"CityMind failed: {exc}",
            ) from exc


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CityMind | Operations Center</title>

<style>
:root {
  --bg: #080d17;
  --panel: #101a2a;
  --surface: #0a1220;
  --line: #26364d;
  --text: #edf3ff;
  --muted: #91a2bb;
  --cyan: #55e6dc;
  --green: #62e5a5;
  --red: #ff8492;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, "Segoe UI", Arial, sans-serif;
  line-height: 1.55;
}

header {
  padding: 19px 5%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  background: #0b1321;
  border-bottom: 1px solid var(--line);
}

.logo {
  font-size: 24px;
  font-weight: 850;
  letter-spacing: 1px;
}

.logo span {
  color: var(--cyan);
}

.live {
  font-size: 11px;
  color: var(--green);
  letter-spacing: 1px;
}

main {
  max-width: 1450px;
  margin: auto;
  padding: 30px 5%;
}

h1 {
  font-size: clamp(26px, 3vw, 36px);
  margin: 0;
}

h2 {
  font-size: 17px;
  margin: 0 0 16px;
}

h3 {
  font-size: 15px;
  margin: 0;
}

.subtitle,
.muted {
  color: var(--muted);
}

.subtitle {
  margin: 7px 0 25px;
}

.muted {
  font-size: 13px;
}

.small {
  font-size: 11px;
}

.layout {
  display: grid;
  grid-template-columns: minmax(280px, .8fr)
                         minmax(0, 1.5fr);
  gap: 20px;
  align-items: start;
}

.panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 15px;
  padding: 21px;
  margin-bottom: 18px;
  min-width: 0;
}

.eyebrow {
  font-size: 10px;
  color: var(--cyan);
  font-weight: 850;
  letter-spacing: 1.6px;
  margin-bottom: 7px;
}

label {
  display: block;
  color: var(--muted);
  font-size: 12px;
  margin: 13px 0 6px;
}

input,
select {
  width: 100%;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 11px;
  font: inherit;
}

input:focus,
select:focus {
  outline: 1px solid var(--cyan);
  border-color: var(--cyan);
}

input[type="checkbox"] {
  width: auto;
  accent-color: var(--cyan);
}

input[type="range"] {
  padding: 0;
  accent-color: var(--cyan);
}

.two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.check {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-top: 14px;
}

.check label {
  margin: 0;
  color: var(--text);
}

.hint {
  font-size: 11px;
  color: var(--muted);
  margin-top: 5px;
}

.primary {
  width: 100%;
  margin-top: 20px;
  padding: 13px;
  border: 0;
  border-radius: 9px;
  background: var(--cyan);
  color: #071519;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.primary:disabled {
  opacity: .6;
  cursor: wait;
}

#progress {
  color: var(--cyan);
  font-size: 12px;
  margin-top: 12px;
}

#error {
  color: var(--red);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  font-size: 12px;
  margin-top: 12px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.metric {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 13px;
  min-width: 0;
}

.metric-label {
  font-size: 10px;
  color: var(--muted);
  display: block;
}

.metric-value {
  font-size: 22px;
  font-weight: 850;
  display: block;
  margin-top: 6px;
  overflow-wrap: anywhere;
}

.stack {
  display: grid;
  gap: 12px;
}

.agent {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px;
  min-width: 0;
}

.agent-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.agent-name {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.agent-icon {
  width: 35px;
  height: 35px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 9px;
  background: #17303c;
  color: var(--cyan);
}

.badge {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 30px;
  font-size: 10px;
  font-weight: 800;
  white-space: nowrap;
}

.good {
  background: #123b30;
  color: var(--green);
}

.warn {
  background: #43242d;
  color: #ffadb5;
}

.neutral {
  background: #202e44;
  color: #b9cbe6;
}

.response {
  color: #c6d4e8;
  font-size: 13px;
  line-height: 1.8;
  overflow-wrap: anywhere;
}

.response p {
  margin: 6px 0;
}

.response ul {
  padding-left: 20px;
}

.response li {
  padding: 3px 0;
}

.hero {
  padding: 23px;
  border: 1px solid #30666c;
  border-radius: 14px;
  background: linear-gradient(135deg, #12323b, #101a2a 85%);
}

.hero-label {
  font-size: 10px;
  color: var(--cyan);
  font-weight: 850;
  letter-spacing: 1.5px;
}

.hero-title {
  font-size: 23px;
  font-weight: 850;
  line-height: 1.4;
  margin: 10px 0;
  overflow-wrap: anywhere;
}

.hero-text {
  font-size: 13px;
  color: #c4d4e8;
  line-height: 1.8;
  overflow-wrap: anywhere;
}

.decision-report {
  display: grid;
  gap: 15px;
}

.decision-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.decision-metric {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 11px;
  padding: 14px;
  min-width: 0;
}

.decision-label {
  font-size: 10px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .5px;
}

.decision-value {
  font-size: 16px;
  font-weight: 800;
  margin-top: 8px;
  overflow-wrap: anywhere;
}

.section {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 11px;
  padding: 17px;
  min-width: 0;
}

.section h3 {
  margin-bottom: 12px;
}

.section p {
  color: #c4d4e8;
  font-size: 13px;
  line-height: 1.8;
  margin: 6px 0;
}

.section li {
  color: #c4d4e8;
  font-size: 13px;
  line-height: 1.8;
}

.action-list {
  display: grid;
  gap: 10px;
}

.action-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: #0d1727;
  border: 1px solid var(--line);
  border-radius: 11px;
  min-width: 0;
  transition: border-color .2s ease;
}

.action-card:hover {
  border-color: #3b777c;
}

.action-number {
  display: grid;
  place-items: center;
  min-width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #17343d;
  color: var(--cyan);
  font-weight: 850;
  font-size: 13px;
}

.action-content {
  flex: 1;
  min-width: 0;
}

.action-content h4 {
  margin: 2px 0 7px;
  font-size: 14px;
}

.action-content p {
  margin: 0;
  color: #c4d4e8;
  font-size: 13px;
  line-height: 1.8;
  overflow-wrap: anywhere;
}

.empty {
  border: 1px dashed #34445b;
  border-radius: 11px;
  padding: 22px;
  color: var(--muted);
  text-align: center;
  font-size: 13px;
}

details {
  margin-top: 10px;
}

summary {
  cursor: pointer;
  color: var(--cyan);
  font-size: 12px;
  font-weight: 750;
}

pre {
  background: #070c15;
  color: #a9bdd8;
  padding: 13px;
  border-radius: 8px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  overflow: auto;
  max-height: 300px;
  font-size: 11px;
}

footer {
  text-align: center;
  padding: 24px;
  color: var(--muted);
  font-size: 11px;
}

@media (max-width: 950px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  header {
    padding: 16px 5%;
  }

  main {
    padding-top: 22px;
  }

  .two,
  .decision-metrics {
    grid-template-columns: 1fr;
  }

  .metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .agent-head {
    align-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
</head>

<body>
<header>
  <div class="logo">CITY<span>MIND</span></div>
  <div class="live">● LOCAL OPERATIONS CENTER</div>
</header>

<main>
  <h1>Smart City Command Center</h1>
  <div class="subtitle">
    Scenario configuration · Agent intelligence · Decision support
  </div>

  <div class="layout">
    <section>
      <div class="panel">
        <div class="eyebrow">01 / INPUT</div>
        <h2>Configure city conditions</h2>

        <form id="form">
          <div class="two">
            <div>
              <label for="city">City</label>
              <input id="city" name="city" value="Chennai" required>
            </div>
            <div>
              <label for="state">State</label>
              <input id="state" name="state" value="Tamil Nadu" required>
            </div>
          </div>

          <div class="two">
            <div>
              <label for="temperature">Temperature (°C)</label>
              <input id="temperature" name="temperature"
                     type="number" value="24" required>
            </div>
            <div>
              <label for="weather">Weather</label>
              <select id="weather" name="weather">
                <option>Heavy rain</option>
                <option>Clear</option>
                <option>Cloudy</option>
                <option>Storm</option>
                <option>Fog</option>
              </select>
            </div>
          </div>

          <label for="traffic">
            Traffic congestion: <span id="trafficText">75%</span>
          </label>
          <input id="traffic" name="traffic_level"
                 type="range" min="0" max="100" value="75">

          <label for="blocked">Blocked roads</label>
          <input id="blocked" name="blocked_roads" value="Road A">
          <div class="hint">Separate multiple roads with commas.</div>

          <div class="check">
            <input id="accident" type="checkbox" checked>
            <label for="accident">Accident reported</label>
          </div>

          <div class="check">
            <input id="emergency" type="checkbox" checked>
            <label for="emergency">Emergency incident active</label>
          </div>

          <div class="two">
            <div>
              <label for="incidentType">Incident type</label>
              <select id="incidentType" name="incident_type">
                <option>accident</option>
                <option>fire</option>
                <option>flood</option>
                <option>medical emergency</option>
                <option>other</option>
              </select>
            </div>
            <div>
              <label for="location">Incident location</label>
              <input id="location" name="incident_location"
                     value="Road A" required>
            </div>
          </div>

          <button id="run" class="primary" type="submit">
            Run CityMind Analysis →
          </button>

          <div id="progress" role="status"></div>
          <div id="error" role="alert"></div>
        </form>
      </div>

      <div class="panel">
        <div class="eyebrow">04 / PERFORMANCE</div>
        <h2>System metrics</h2>

        <div class="metrics">
          <div class="metric">
            <span class="metric-label">Agent calls</span>
            <strong class="metric-value" id="mAgents">—</strong>
          </div>
          <div class="metric">
            <span class="metric-label">MCP calls</span>
            <strong class="metric-value" id="mMcp">—</strong>
          </div>
          <div class="metric">
            <span class="metric-label">Replanning</span>
            <strong class="metric-value" id="mReplan">—</strong>
          </div>
          <div class="metric">
            <span class="metric-label">Total runs</span>
            <strong class="metric-value" id="mRuns">—</strong>
          </div>
          <div class="metric">
            <span class="metric-label">Approval flags</span>
            <strong class="metric-value" id="mApproval">—</strong>
          </div>
          <div class="metric">
            <span class="metric-label">Runtime</span>
            <strong class="metric-value" id="mRuntime">—</strong>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="panel">
        <div class="eyebrow">02 / AGENT INTELLIGENCE</div>
        <h2>Specialist agent reports</h2>
        <p class="muted">
          Structured summaries of actual agent responses.
        </p>
        <div id="agents" class="stack">
          <div class="empty">
            Run an analysis to see agent reports.
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="eyebrow">03 / SYSTEM DECISION</div>
        <h2>Final recommendation</h2>

        <div id="status">
          <span class="badge neutral">Awaiting analysis</span>
        </div>

        <div id="result" style="margin-top:15px">
          <div class="empty">
            Run a scenario to generate the formatted system decision.
          </div>
        </div>

        <div id="approvalNote" class="muted"
             style="margin-top:12px"></div>
      </div>

      <div class="panel">
        <div class="eyebrow">TECHNICAL DETAILS</div>
        <h2>Original system output</h2>
        <p class="muted">
          Hidden by default; available for debugging.
        </p>
        <details>
          <summary>Expand raw output</summary>
          <pre id="raw">No run yet.</pre>
        </details>
      </div>
    </section>
  </div>
</main>

<footer>
  CityMind · Simulated city data · No live municipal actions are performed
</footer>

<script>
const form = document.getElementById("form");
const runButton = document.getElementById("run");

document.getElementById("traffic").addEventListener("input", event => {
  document.getElementById("trafficText").textContent =
    event.target.value + "%";
});


function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[char]);
}


function list(items) {
  if (!Array.isArray(items) || !items.length) {
    return '<p class="muted">No additional information provided.</p>';
  }

  return "<ul>" + items.map(item =>
    `<li>${esc(item)}</li>`
  ).join("") + "</ul>";
}


function showAgents(cards) {
  const root = document.getElementById("agents");
  root.replaceChildren();

  if (!Array.isArray(cards) || !cards.length) {
    root.innerHTML =
      '<div class="empty">No formatted agent reports were returned.</div>';
    return;
  }

  const icons = {
    traffic: "↗",
    weather: "☁",
    emergency: "✚"
  };

  for (const agent of cards) {
    const name = String(agent.name || "Specialist agent");
    const lower = name.toLowerCase();
    const key = Object.keys(icons).find(item => lower.includes(item));

    const card = document.createElement("div");
    card.className = "agent";

    card.innerHTML = `
      <div class="agent-head">
        <div class="agent-name">
          <div class="agent-icon">${key ? icons[key] : "◈"}</div>
          <div>
            <h3>${esc(name)}</h3>
            <span class="muted small">
              ${esc(agent.status || "Report received")}
            </span>
          </div>
        </div>
        <span class="badge good">Report received</span>
      </div>

      <div class="response">
        <p>${esc(agent.summary || "No summary provided.")}</p>
        ${list(agent.findings)}
      </div>
    `;

    root.append(card);
  }
}


/*
Split a numbered list if the model accidentally returns it
as a single paragraph instead of separate next_steps items.
*/
function splitNumberedActions(value) {
  const text = String(value || "").trim();

  if (!text) {
    return [];
  }

  const normalized = text
    .replace(/\r/g, "")
    .replace(/(?<!^)\s+(?=\d+[.)]\s+)/g, "\n");

  const lines = normalized
    .split(/\n+/)
    .map(line => line.trim())
    .filter(Boolean);

  const matches = lines.map(line =>
    line.match(/^\d+[.)]\s*(.+)$/)
  );

  if (matches.length > 1 && matches.every(Boolean)) {
    return matches.map(match => match[1].trim());
  }

  return [];
}


function showDecision(presentation, approvalRequired) {
  const root = document.getElementById("result");

  if (!presentation) {
    root.innerHTML = `
      <div class="section">
        <h3>Report formatting unavailable</h3>
        <p>
          The formatter did not return a structured report.
          Check the backend error message and try again.
        </p>
      </div>
    `;
    return;
  }

  let actions = Array.isArray(presentation.next_steps)
    ? presentation.next_steps.map(String)
    : [];

  let recommendation = String(
    presentation.recommended_action || ""
  );

  // Fallback for old-style output containing numbered actions
  // in a single paragraph.
  if (actions.length <= 1) {
    const combined = actions.length
      ? actions[0]
      : recommendation;

    const extracted = splitNumberedActions(combined);

    if (extracted.length > 1) {
      actions = extracted;
      recommendation = "";
    }
  }

  if (
    !recommendation ||
    /^\s*\d+[.)]\s/.test(recommendation)
  ) {
    recommendation =
      "Review the individual recommended actions below.";
  }

  const facts = [
    ["Recommended route", presentation.route],
    ["Response estimate", presentation.response_time],
    ["Risk level", presentation.risk_level]
  ];

  const risk = String(
    presentation.risk_level || ""
  ).toLowerCase();

  const riskClass = ["high", "critical"].some(value =>
    risk.includes(value)
  ) ? "warn" : risk === "low" ? "good" : "neutral";

  const actionsHTML = actions.length
    ? actions.map((item, index) => `
        <div class="action-card">
          <div class="action-number">
            ${String(index + 1).padStart(2, "0")}
          </div>
          <div class="action-content">
            <h4>Action ${index + 1}</h4>
            <p>
              ${esc(String(item).replace(/^\d+[.)]\s*/, ""))}
            </p>
          </div>
        </div>
      `).join("")
    : '<p class="muted">No separate action items were provided.</p>';

  root.innerHTML = `
    <div class="decision-report">

      <div class="hero">
        <div class="hero-label">
          CITYMIND / SUPERVISOR ASSESSMENT
        </div>

        <div class="hero-title">
          ${esc(presentation.headline || "City situation assessment")}
        </div>

        <div class="hero-text">
          ${esc(recommendation)}
        </div>
      </div>

      <div class="decision-metrics">
        ${facts.map(([name, value]) => `
          <div class="decision-metric">
            <div class="decision-label">${esc(name)}</div>
            <div class="decision-value">
              ${
                name === "Risk level" && value
                  ? `<span class="badge ${riskClass}">${esc(value)}</span>`
                  : esc(value || "Not provided")
              }
            </div>
          </div>
        `).join("")}
      </div>

      <div class="section">
        <div class="eyebrow">RESPONSE PLAN</div>
        <h3>Recommended actions</h3>
        <div class="action-list">
          ${actionsHTML}
        </div>
      </div>

      <div class="section">
        <div class="eyebrow">SUPPORTING ANALYSIS</div>
        <h3>Why this recommendation?</h3>
        ${list(presentation.reasoning)}
      </div>

      <div class="section">
        <h3>Limitations and uncertainties</h3>
        ${list(presentation.limitations)}
      </div>
    </div>
  `;

  document.getElementById("status").innerHTML =
    approvalRequired
      ? '<span class="badge warn">Human review required</span>'
      : '<span class="badge good">Analysis complete</span>';

  document.getElementById("approvalNote").textContent =
    approvalRequired
      ? "The configured approval check flagged the supervisor output. Review it before taking action."
      : "No configured high-risk phrase was detected. This does not guarantee safety.";
}


function showMetrics(metrics = {}) {
  const mapping = {
    mAgents: "agent_calls",
    mMcp: "mcp_calls",
    mReplan: "replanning_events",
    mRuns: "run_count",
    mApproval: "approval_required"
  };

  for (const [elementId, key] of Object.entries(mapping)) {
    document.getElementById(elementId).textContent =
      metrics[key] ?? 0;
  }

  const runtime = metrics.total_runtime_seconds;

  document.getElementById("mRuntime").textContent =
    runtime == null
      ? "—"
      : Number(runtime).toFixed(2) + "s";
}


form.addEventListener("submit", async event => {
  event.preventDefault();

  const errorBox = document.getElementById("error");
  const progress = document.getElementById("progress");

  errorBox.textContent = "";
  progress.textContent =
    "Running agents, supervisor, and report formatter...";

  runButton.disabled = true;
  runButton.textContent = "Processing...";

  const data = Object.fromEntries(
    new FormData(form).entries()
  );

  data.temperature = Number(data.temperature);
  data.traffic_level = Number(data.traffic_level);

  data.blocked_roads = data.blocked_roads
    .split(",")
    .map(road => road.trim())
    .filter(Boolean);

  data.accident =
    document.getElementById("accident").checked;

  data.emergency_incident =
    document.getElementById("emergency").checked;

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "CityMind run failed."
      );
    }

    showAgents(result.presentation?.agent_cards);

    showDecision(
      result.presentation,
      result.approval_required
    );

    showMetrics(result.metrics);

    document.getElementById("raw").textContent =
      JSON.stringify(result.technical, null, 2);

    progress.textContent =
      "Analysis and report formatting completed.";

  } catch (error) {
    errorBox.textContent = error.message;
    progress.textContent = "";

  } finally {
    runButton.disabled = false;
    runButton.textContent = "Run CityMind Analysis →";
  }
});
</script>
</body>
</html>
"""
