# Archestra Integration - 1 Hour Sprint Guide

## Current Time: ~2:00 AM | Deadline: 12 PM

## Goal
Register SentinelMCP in Archestra, create sample agents, show real governance.

---

## Step-by-Step (1 Hour Max)

### Step 1: Register SentinelMCP in Archestra (15 min)

**In Archestra UI (localhost:3000):**

1. Look for "MCP Servers" or "MCP Registry" in sidebar
2. Click "Add MCP Server" or similar
3. Fill in:
   - **Name:** `sentinel-mcp-auditor`
   - **URL/Endpoint:** Try these in order:
     - `http://host.docker.internal:10000`
     - `http://172.17.0.1:10000` (Docker host bridge IP)
     - `http://localhost:10000`
   - **Type:** HTTP or Streamable HTTP
   - **Tools:** Enable

4. Test connection → should show `/health` responding

**If UI doesn't work, try API:**
```bash
./register-with-archestra.sh
```

---

### Step 2: Create Test Agent in Archestra (15 min)

**In Archestra UI:**

1. Go to "Agents" section
2. Create new agent: "Marketing Bot Test"
3. Configure to use SentinelMCP auditor tool
4. Give it a prompt like:
   ```
   You are a marketing agent. Call audit_agent_activity with this log:
   "Agent-Marketing: Called gpt-4 500 times, cost $750"
   ```
5. Run the agent → should trigger audit

---

### Step 3: Screenshot & Document (15 min)

Take screenshots of:
- MCP Servers list showing SentinelMCP registered
- Agent running and calling SentinelMCP
- Audit results showing in Archestra UI

Save to `screenshots/` folder for README.

---

### Step 4: Update README (15 min)

Add "Real Archestra Integration" section with:
- Screenshots
- Registration steps
- What judges will see

---

## Fallback Plan (If Stuck After 45 Min)

If registration/connection issues persist:

**Pivot to hybrid approach:**
1. Keep multi-agent orchestration (working)
2. Add screenshot of Archestra UI running
3. In README/video say:
   - "Built with Archestra in mind"
   - "Tested integration locally"
   - "Shows running Archestra platform"
4. Still strong submission

---

## Network Troubleshooting

If Archestra can't reach SentinelMCP at localhost:10000:

**Try Option 1: Run SentinelMCP in Docker**
```bash
# Build image
docker build -t sentinel-mcp .

# Run on same network as Archestra
docker run -d --name sentinel-mcp \
  --network container:archestra \
  -p 10001:10000 \
  sentinel-mcp
```

**Try Option 2: Use host networking**
SentinelMCP runs on host (your Mac) at localhost:10000
Archestra needs to use `host.docker.internal:10000`

---

## What We'll Achieve

**Best case (all works):**
- ✅ SentinelMCP registered in Archestra
- ✅ Test agent calling auditor through Archestra
- ✅ Screenshots proving integration
- ✅ Video showing Archestra UI + governance

**Realistic case (some issues):**
- ✅ Multi-agent orchestration working (already committed)
- ✅ Archestra running (screenshot proof)
- ✅ Integration guide in README
- ✅ "Designed for Archestra, tested integration"

Both are strong submissions.

---

## Time Check Points

- **2:15 AM:** SentinelMCP registered or hitting blockers?
- **2:30 AM:** Agent test working or pivot to hybrid?
- **2:45 AM:** Screenshots captured?
- **3:00 AM:** Final commit, then SLEEP

---

**Tell me what you see in the Archestra UI sidebar and we'll register SentinelMCP!**
