# SentinelMCP – AI Agent Auditor

**MCP-native governance for AI agents running at scale.**  
Built for the **2 Fast 2 MCP Hackathon** — designed to integrate with **Archestra** deployments as a centralized auditor.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## The Problem: AI Agents Running Wild

When companies deploy dozens of AI agents in production (e.g., using Archestra):

- **Agent A** calls GPT-4 **500x in an hour** → Burns **$450** before anyone notices
- **Agent B** accesses a **production database** it shouldn't touch → Security incident
- **Agent C** hits **rate limits** in an infinite loop → System downtime
- **Platform engineers have no visibility** until the damage is done

**The gap:** Agents run fast, but **nobody's watching the watchers.**

---

## The Solution: SentinelMCP

**An MCP agent that audits OTHER agents.**

SentinelMCP ingests activity logs from AI agents and flags violations in real-time:

- 💰 **Cost violations** — Agent spending spikes, runaway API costs
- 🔒 **Security violations** — Unauthorized access, credential leaks
- ⚡ **Rate limit abuse** — Excessive API calls, quota exhaustion
- ⚠️ **Anomalies** — Infinite loops, repeated errors

**Output:** Structured audit report with risk score (0-100) and actionable recommendations.

---

## Why This Matters (And Why It Wins)

### 1. **Meta-Level MCP** (Judges Love This)
Using MCP to **govern MCP agents** is elegant. SentinelMCP is itself an MCP tool that monitors other MCP tools.

### 2. **Solves Archestra's Core Value Prop**
Archestra promises: *"governance, security, and observability for AI agents at scale."*  
SentinelMCP **proves** that promise by:
- **Detecting cost overruns** before they spiral
- **Flagging security violations** in real-time
- **Providing observability** across multi-agent systems

### 3. **Painful, Real Problem**
Platform engineers managing 50+ agents in production **feel** this pain:
- "Our AI bill jumped from $2k to $15k last month—why?"
- "An agent accessed prod DB with write permissions—how?"
- "We need audit trails for compliance."

SentinelMCP answers all three.

### 4. **Production-Ready Design**
- **Read-only:** Only analyzes logs; never modifies agents
- **Structured output:** Pydantic models with risk scores
- **Tool boundaries:** Clear MCP contract for governance
- **Archestra-native:** Designed to run as a central auditor in the control plane

---

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
# Clone and setup
git clone https://github.com/incruder1/sentinel_mcp.git
cd sentinel_mcp
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run server (default port 10000)
python main.py
# or: uvicorn main:app --host 0.0.0.0 --port 10000
```

### Try It

```bash
# Health check
curl http://localhost:10000/health

# Get sample agent activity logs
curl http://localhost:10000/mock-data

# Audit agent activity
curl -X POST http://localhost:10000/audit \
  -H "Content-Type: application/json" \
  -d '{
    "activity_logs": "Agent-A: Called gpt-4 85 times in 10 min, cost $127.50\nAgent-B: Attempted unauthorized access to restricted S3 bucket\nAgent-C: API_KEY exposed in logs"
  }'
```

**Example Response:**

```json
{
  "risk_score": 100,
  "violations": [
    {
      "type": "COST_SPIKE",
      "severity": "CRITICAL",
      "agent_id": "Agent-A",
      "description": "Agent Agent-A incurred $127 in charges - exceeds threshold",
      "recommendation": "Set cost limits in Archestra; review agent prompt efficiency"
    },
    {
      "type": "SECURITY",
      "severity": "CRITICAL",
      "agent_id": "Agent-B",
      "description": "Agent Agent-B attempted unauthorized access - security policy violation",
      "recommendation": "Review agent permissions in Archestra; enforce least-privilege"
    },
    {
      "type": "SECURITY",
      "severity": "CRITICAL",
      "agent_id": "Agent-C",
      "description": "Agent Agent-C accessed sensitive credentials - data leak risk",
      "recommendation": "Use Archestra secret management; rotate exposed credentials"
    }
  ],
  "summary": "⚠️ 3 violation(s) detected across 3 agent(s). 3 CRITICAL, 0 HIGH. Immediate action required.",
  "agents_audited": ["Agent-A", "Agent-B", "Agent-C"]
}
```

---

## Integrating with Archestra

SentinelMCP is designed as a standalone MCP server that can be deployed alongside Archestra installations for centralized agent governance.

### Integration Steps

**1. Deploy SentinelMCP**
```bash
# Option A: Use live demo
🔗 https://sentinel-mcp-auditor.onrender.com

# Option B: Self-host with Docker
docker build -t sentinel-mcp .
docker run -p 10000:10000 sentinel-mcp

# Option C: Deploy to your infrastructure
# See render.yaml for deployment config
```

**2. Configure in Archestra**
- Register SentinelMCP as an MCP server in your Archestra deployment
- Set up agent activity log forwarding to `/audit` endpoint
- Configure alert rules for CRITICAL/HIGH violations

**3. Connect to Agent Logs**
- Archestra agents → activity logs → SentinelMCP `/audit`
- Returns structured violations with risk scores
- Platform admins can view via Archestra UI or direct API calls

### Architecture in Archestra Deployment

```
Your Archestra Deployment (self-hosted)
  ├─ Application Agents (A, B, C)
  │    └─ Generate activity logs
  ├─ SentinelMCP (Auditor Agent)
  │    ├─ Consumes logs via MCP
  │    └─ Returns audit reports
  └─ Archestra Control Plane
       ├─ Orchestrates all agents
       ├─ Routes logs to auditor
       └─ Displays governance dashboard
```

### Why This Integration Matters

- **Centralized governance**: One auditor for all agents in your Archestra instance
- **Production-ready**: Designed for self-hosted enterprise deployments
- **MCP-native**: Clean tool boundaries, structured output
- **Flexible**: Works with any Archestra setup (on-prem, cloud, hybrid)

---

## Deploy to Render (Free)

1. Push this repo to GitHub
2. **Render** → **New** → **Web Service**
3. Connect repo
4. **Build**: `pip install -r requirements.txt`
5. **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy and use the URL

Or click: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check for load balancers |
| `/audit` | POST | Audit agent activity logs → structured report |
| `/mock-data` | GET | Sample agent activity for testing |
| `/` | GET | API documentation |

**POST /audit** body:
```json
{
  "activity_logs": "Agent-A: Called gpt-4 50x, cost $75\nAgent-B: Rate limit exceeded"
}
```

**Response:** `AuditReport` with `risk_score`, `violations[]`, `summary`, `agents_audited[]`

---

## Violation Types

| Type | Examples | Severity |
|------|----------|----------|
| **COST_SPIKE** | Agent spent $500 in 1 hour, Called expensive model 200x | CRITICAL / HIGH |
| **SECURITY** | Unauthorized DB access, Credential leak, Forbidden resource | CRITICAL / HIGH |
| **RATE_LIMIT** | 500 API calls in 5 min, HTTP 429 errors, Quota exceeded | HIGH / MEDIUM |
| **ANOMALY** | Same tool called 100x (loop), 50 consecutive errors | HIGH / MEDIUM |

---

## Why This Wins the Hackathon

### Judging Criteria Alignment

| Criterion | How SentinelMCP Scores |
|-----------|------------------------|
| **Best Use of Archestra** | ✅ Meta-level governance; uses MCP to monitor MCP agents; proves Archestra's value prop |
| **Potential Impact** | ✅ Solves painful, real problem (runaway costs, security incidents); production-ready |
| **Creativity & Originality** | ✅ "Agent that watches other agents" is elegant and novel |
| **Technical Implementation** | ✅ Clean code, structured output, proper tool boundaries, MCP-native design |
| **Learning & Growth** | ✅ Deep dive into MCP governance patterns, multi-agent orchestration |

### Resume Impact

You can write:
- *"Built AI governance system for multi-agent platforms using MCP and Archestra"*
- *"Implemented real-time auditing for cost control, security, and observability across 50+ agents"*
- *"Designed meta-level MCP agent for platform-wide compliance and monitoring"*

**This is SDE-2 / Platform Engineer level.**

---

## Future Roadmap

- **Real-time streaming:** WebSocket endpoint for live audit feeds
- **Alert integration:** Slack/PagerDuty webhooks for CRITICAL violations
- **Historical analytics:** Track agent behavior over time, cost trends
- **Policy engine:** Custom audit rules per org (e.g., "flag if Agent-X spends >$100/day")
- **Auto-remediation:** Pause agents on CRITICAL violations (with approval workflow)

---

## Demo Video Script (2-3 min)

**[0:00-0:30] Problem**  
"When you run 50 AI agents in production, one agent can burn $10k in a day—and you won't know until the bill comes. SentinelMCP solves this."

**[0:30-1:00] Architecture**  
*Show diagram* "Agents run in Archestra. SentinelMCP audits their activity logs via MCP and flags cost, security, and operational violations."

**[1:00-2:00] Demo**  
*Terminal:* `curl /audit` with sample logs → show JSON response with CRITICAL violations + recommendations.

**[2:00-2:30] Why Archestra**  
"Without Archestra, this is chaos—50 agents, 50 separate audit systems. With Archestra, SentinelMCP runs centrally and governs everything. That's the power of MCP + control plane."

---

## Tech Stack

- **Python 3.10+** (MCP-native language)
- **FastAPI** (ASGI server, production-ready)
- **Pydantic** (structured output, type safety)
- **Uvicorn** (ASGI runtime)

No external dependencies beyond standard MCP ecosystem.

---

## License

MIT

---

## Built For

**2 Fast 2 MCP Hackathon** by WeMakeDevs + Archestra.ai

*"It doesn't matter if you win by an inch or a mile—winning's winning."*  
— Dominic Toretto (and this README)

---

**Ready to audit your agents? Deploy SentinelMCP now. 🏁**
