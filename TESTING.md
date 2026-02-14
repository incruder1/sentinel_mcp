# 🧪 Testing Guide for SentinelMCP

## Quick Start (Choose One Method)

### Option 1: Instant Test (No Server) ⚡
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate
python test_interactive.py
```
**Time:** 5 seconds  
**Tests:** Core audit logic with 6 scenarios

---

### Option 2: Quick Server Test 🚀
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate
./test_quick.sh
```
**Time:** 10 seconds  
**Tests:** Server health + one audit scenario

---

### Option 3: Full Demo 🎬
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate

# Terminal 1: Start server
python main.py

# Terminal 2 (new tab): Run demo
python demo.py
```
**Time:** 2 minutes  
**Tests:** 5 comprehensive scenarios with formatted output

---

### Option 4: API Testing (curl) 🔧

**Step 1:** Start server
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate
python main.py
```

**Step 2:** In a new terminal, run tests
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate
./test_api.sh
```

Or manually:
```bash
# Health check
curl http://localhost:10000/health

# Get sample data
curl http://localhost:10000/mock-data

# Test audit
curl -X POST http://localhost:10000/audit \
  -H "Content-Type: application/json" \
  -d '{
    "activity_logs": "Agent-A: Called gpt-4 500 times, cost $750\nAgent-B: Attempted unauthorized access"
  }'
```

---

## What Each Test Does

### test_interactive.py
- ✅ Tests core `audit_agent_activity()` function
- ✅ 6 scenarios: cost, security, rate limit, anomaly, healthy, multi-agent
- ✅ Shows violations with descriptions and recommendations
- ✅ No server needed

### test_quick.sh
- ✅ Starts server automatically
- ✅ Tests `/health` endpoint
- ✅ Tests `/audit` with violations
- ✅ Auto-cleanup (kills server)

### demo.py
- ✅ Full demo with 5 scenarios
- ✅ Formatted output with emojis
- ✅ Shows all violation types
- ✅ Production-quality demo for video

### test_api.sh
- ✅ Tests all API endpoints
- ✅ Health, mock-data, audit
- ✅ Multiple scenarios
- ✅ JSON formatted output

---

## Expected Output Examples

### Healthy System (No Violations)
```json
{
  "risk_score": 0,
  "violations": [],
  "summary": "✅ No violations detected. Audited 1 agent(s). System healthy.",
  "agents_audited": ["Agent-E"]
}
```

### Critical Violations
```json
{
  "risk_score": 100,
  "violations": [
    {
      "type": "COST_SPIKE",
      "severity": "CRITICAL",
      "agent_id": "Agent-A",
      "description": "Agent Agent-A incurred $750 in charges - exceeds threshold",
      "recommendation": "Set cost limits in Archestra; review agent prompt efficiency"
    },
    {
      "type": "SECURITY",
      "severity": "CRITICAL",
      "agent_id": "Agent-B",
      "description": "Agent Agent-B attempted unauthorized access - security policy violation",
      "recommendation": "Review agent permissions in Archestra; enforce least-privilege"
    }
  ],
  "summary": "⚠️ 2 violation(s) detected across 2 agent(s). 2 CRITICAL, 0 HIGH. Immediate action required.",
  "agents_audited": ["Agent-A", "Agent-B"]
}
```

---

## Custom Testing

Want to test your own logs? Use Python:

```python
from tools import audit_agent_activity

# Your custom logs
logs = """
Agent-MyBot: Called gpt-4 200 times, cost $300
Agent-MyBot: Accessed restricted database
"""

# Run audit
report = audit_agent_activity(logs)

# Print results
print(f"Risk Score: {report.risk_score}/100")
print(f"Summary: {report.summary}")
for v in report.violations:
    print(f"- [{v.severity}] {v.type}: {v.description}")
```

Or use curl with the server:

```bash
curl -X POST http://localhost:10000/audit \
  -H "Content-Type: application/json" \
  -d '{
    "activity_logs": "YOUR LOGS HERE"
  }' | python -m json.tool
```

---

## Troubleshooting

### Server won't start
```bash
# Check if port 10000 is in use
lsof -i :10000

# Kill existing process
kill -9 <PID>

# Or use different port
PORT=8000 python main.py
```

### "Module not found"
```bash
# Make sure venv is activated
source .venv/bin/activate

# Verify packages installed
pip list | grep -E "fastapi|uvicorn|pydantic"
```

### curl fails
```bash
# Check server is running
curl http://localhost:10000/health

# If fails, check server logs in Terminal 1
```

---

## For Demo Video

**Best command to record:**
```bash
python demo.py
```

Shows:
- Professional formatted output
- All violation types
- Clear narrative flow
- Good for screen recording

---

## Before Submission

Run this final check:
```bash
cd /Users/devjohri/Documents/personal/sentinel_mcp
source .venv/bin/activate

echo "1. Testing core logic..."
python test_interactive.py > /dev/null && echo "✅ Core logic works"

echo "2. Testing API..."
python main.py &
SERVER_PID=$!
sleep 3
curl -s http://localhost:10000/health > /dev/null && echo "✅ Server works"
kill $SERVER_PID

echo "3. All files present..."
ls main.py tools.py demo.py README.md requirements.txt > /dev/null && echo "✅ All files present"

echo ""
echo "🎉 Ready to deploy and submit!"
```

---

## Quick Reference

| Command | What It Tests | Time |
|---------|--------------|------|
| `python test_interactive.py` | Core logic only | 5s |
| `./test_quick.sh` | Server + one scenario | 10s |
| `python demo.py` | Full demo (5 scenarios) | 2m |
| `./test_api.sh` | All API endpoints | 30s |

**Recommendation for now:** Run `python test_interactive.py` — fastest way to verify everything works.
