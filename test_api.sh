#!/bin/bash
# API Testing Script for SentinelMCP

echo "🚀 SentinelMCP API Testing"
echo "=========================="
echo ""

BASE_URL="http://localhost:10000"

# Test 1: Health check
echo "Test 1: Health Check"
echo "curl $BASE_URL/health"
curl -s $BASE_URL/health | python -m json.tool
echo ""
echo ""

# Test 2: Get mock data
echo "Test 2: Get Sample Data"
echo "curl $BASE_URL/mock-data"
curl -s $BASE_URL/mock-data | python -m json.tool | head -20
echo ""
echo ""

# Test 3: Audit with cost violation
echo "Test 3: Cost Spike Detection"
echo 'curl -X POST $BASE_URL/audit -d {"activity_logs": "..."}'
curl -s -X POST $BASE_URL/audit \
  -H "Content-Type: application/json" \
  -d '{"activity_logs": "Agent-A: Called gpt-4 500 times in 10 min, cost $750"}' \
  | python -m json.tool
echo ""
echo ""

# Test 4: Security violation
echo "Test 4: Security Violation Detection"
curl -s -X POST $BASE_URL/audit \
  -H "Content-Type: application/json" \
  -d '{"activity_logs": "Agent-B: Attempted unauthorized access to production database\nAgent-B: API_KEY exposed in logs"}' \
  | python -m json.tool
echo ""
echo ""

# Test 5: Multi-agent chaos
echo "Test 5: Multi-Agent Crisis"
curl -s -X POST $BASE_URL/audit \
  -H "Content-Type: application/json" \
  -d '{"activity_logs": "Agent-A: Called gpt-4 850 times, cost $1,240\nAgent-B: Database write operation\nAgent-C: API_KEY exposed\nAgent-D: Rate limit exceeded"}' \
  | python -m json.tool
echo ""
echo ""

echo "✅ API Testing Complete!"
