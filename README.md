# SentinelMCP – AI Agent Auditor

MCP-based governance for AI agents: audit activity logs for cost spikes, security issues, rate limits, and anomalies. Built for the **2 Fast 2 MCP** hackathon; integrates with **Archestra** as an MCP server.

**Live demo:** [sentinel-mcp-auditor.onrender.com](https://sentinel-mcp-auditor.onrender.com)  
**Repo:** [github.com/incruder1/sentinel_mcp](https://github.com/incruder1/sentinel_mcp)

---

## What it does

You send agent activity logs (plain text). SentinelMCP returns a structured report:

- **Risk score** (0–100)
- **Violations** with type (COST_SPIKE, SECURITY, RATE_LIMIT, ANOMALY), severity, description, and recommendation
- **Agents audited** and a short summary

It runs as a REST API and as an MCP server so Archestra (or any MCP client) can call the audit tool.

---

## Tech stack

- **Python 3.10+**, **FastAPI**, **Pydantic**, **Uvicorn**
- **MCP SDK** for the Archestra-facing server
- **OpenAI** (optional) for LLM-based audit when you set `OPENAI_API_KEY`

**Architecture:** Two entrypoints. `main.py` runs the web app and REST API (e.g. on Render). `mcp_server.py` runs the MCP server (e.g. locally for Archestra). Both use the same audit logic in `tools.py`. Audit is rule-based by default; optional `use_ai=true` uses an LLM for messier logs.


## Architecture

### Before SentinelMCP
```
Archestra Platform
  ├─ Agent A → calls gpt-4 500x → burns $450 💸
  ├─ Agent B → accesses prod DB → security risk 🔓
  └─ Agent C → infinite loop → nobody notices ♾️
```

### With SentinelMCP
```
┌────────────────────────────────────────────────────────────┐
│                  Archestra Control Plane                    │
│         Central execution • Permissions • Observability     │
└────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
  ┌─────────┐          ┌─────────┐         ┌─────────┐
  │ Agent A │          │ Agent B │         │ Agent C │
  │ (App)   │          │ (App)   │         │ (App)   │
  └─────────┘          └─────────┘         └─────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │ activity logs
                             ▼
                    ┌─────────────────┐
                    │  SentinelMCP    │
                    │    (Auditor)    │
                    └─────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Audit Report      │
                  │ • Risk Score: 95/100│
                  │ • 3 CRITICAL issues │
                  │ • Recommendations   │
                  └─────────────────────┘
```

**Key:** SentinelMCP runs **inside Archestra** as a governance layer. All agent activity flows through audit checks.

---

## Security & Governance Features

| Feature | Implementation |
|---------|----------------|
| **Tool-level isolation** | SentinelMCP has ONE function: `audit_agent_activity()` |
| **Read-only** | Only reads logs; cannot modify agents or infrastructure |
| **Structured output** | Pydantic models; no free-form agent actions |
| **Multi-agent observability** | Tracks violations across all agents in one report |
| **Cost control** | Flags spending thresholds before bills explode |
| **Security enforcement** | Detects unauthorized access, credential leaks |
| **Archestra-native** | Designed as control plane component, not standalone |

---

## Quick Start

### Local

```bash
git clone https://github.com/incruder1/sentinel_mcp.git
cd sentinel_mcp
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Open **http://localhost:10000** for the UI, or call the API:

```bash
curl http://localhost:10000/health
curl -X POST http://localhost:10000/audit -H "Content-Type: application/json" \
  -d '{"activity_logs": "Agent-X: cost $500 in 1hr\nAgent-Y: API_KEY exposed in logs"}'
```

**Quick demo (CLI):** With the server running, `python demo.py` runs several audit scenarios against the API. For the multi-agent orchestrator: `python orchestrator.py` (uses the same `/audit` endpoint).

---

## Project structure

| Path | Purpose |
|------|---------|
| `main.py` | FastAPI app: web UI, `/audit`, `/health`, `/mock-data` |
| `mcp_server.py` | Standalone MCP server for Archestra (port 10001) |
| `tools.py` | Audit logic: rules + optional LLM audit |
| `static/index.html` | Frontend for live audit demo |
| `demo.py` | CLI script: runs preset scenarios against API |
| `orchestrator.py` | Runs mock agents and audits their output |
| `agents/*.py` | Mock agents used by orchestrator |
| `render.yaml` | Render blueprint; `Dockerfile` for container deploy |

---

## Archestra integration

1. Run the MCP server: `python mcp_server.py` (listens on port 10001).
2. In Archestra, add an MCP server with URL `http://host.docker.internal:10001/mcp` (or your host:10001/mcp).
3. The `audit_agent_activity_tool` appears in the tool list; agents or the chat can call it with `activity_logs` and get an audit report.

---

## API

| Endpoint    | Method | Description |
|------------|--------|-------------|
| `/`        | GET    | Web UI      |
| `/health`  | GET    | Health check |
| `/audit`   | POST   | Body: `{ "activity_logs": "..." }`. Optional: `"use_ai": true` for LLM audit (needs `OPENAI_API_KEY`). |
| `/mock-data` | GET | Sample logs for testing |

---

## Violation types

| Type        | Examples |
|------------|----------|
| COST_SPIKE | High spend, $ amounts, billing keywords |
| SECURITY   | Unauthorized access, credentials, DB writes, admin |
| RATE_LIMIT | 429, throttle, quota, excessive requests |
| ANOMALY    | Same tool many times, consecutive errors, retries, stuck/crash |

---

## Deploy (Render)

Connect the repo to Render as a Web Service. Build: `pip install -r requirements.txt`. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Health path: `/health`. See `render.yaml` for a blueprint.

---


## Future Roadmap

- **Real-time streaming:** WebSocket endpoint for live audit feeds
- **Alert integration:** Slack/PagerDuty webhooks for CRITICAL violations
- **Historical analytics:** Track agent behavior over time, cost trends
- **Policy engine:** Custom audit rules per org (e.g., "flag if Agent-X spends >$100/day")
- **Auto-remediation:** Pause agents on CRITICAL violations (with approval workflow)

---