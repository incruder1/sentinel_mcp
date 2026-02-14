#!/bin/bash
echo "🚀 Quick SentinelMCP Test"
echo "=========================="
echo ""
echo "Starting server..."
source .venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 10000 >/dev/null 2>&1 &
SERVER_PID=$!
sleep 3

echo "✓ Server running (PID: $SERVER_PID)"
echo ""
echo "Test 1: Health check"
curl -s http://127.0.0.1:10000/health | python -m json.tool
echo ""
echo ""
echo "Test 2: Audit with CRITICAL violations"
curl -s -X POST http://127.0.0.1:10000/audit \
  -H "Content-Type: application/json" \
  -d '{"activity_logs": "Agent-A: Called gpt-4 500 times in 10 min, cost $750\nAgent-B: Attempted unauthorized access to production database\nAgent-C: API_KEY exposed in logs"}' \
  | python -m json.tool

echo ""
echo "✓ Tests complete"
kill $SERVER_PID 2>/dev/null
