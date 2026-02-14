#!/bin/bash
# Complete Testing Guide for SentinelMCP

echo "========================================"
echo "SentinelMCP - Complete Testing Suite"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Test 1: Live Deployment${NC}"
echo "Testing https://sentinel-mcp-auditor.onrender.com"
echo ""

HEALTH_CHECK=$(curl -s https://sentinel-mcp-auditor.onrender.com/health)
if echo "$HEALTH_CHECK" | grep -q "ok"; then
    echo -e "${GREEN}✓ Live deployment is UP${NC}"
    echo "$HEALTH_CHECK" | python3 -m json.tool
else
    echo -e "${RED}✗ Live deployment is DOWN${NC}"
fi
echo ""

echo "----------------------------------------"
echo -e "${BLUE}Test 2: API Endpoint Tests${NC}"
echo ""

# Test Cost Spike Scenario
echo "Testing Cost Spike scenario..."
COST_TEST=$(curl -s -X POST https://sentinel-mcp-auditor.onrender.com/audit \
  -H "Content-Type: application/json" \
  -d '{"activity_logs":"[2024-02-14] agent-marketing: API call cost: $45.20\n[2024-02-14] agent-marketing: API call cost: $52.10"}')

if echo "$COST_TEST" | grep -q "risk_score"; then
    echo -e "${GREEN}✓ API is working${NC}"
    echo "Risk score found in response"
else
    echo -e "${RED}✗ API test failed${NC}"
fi
echo ""

echo "----------------------------------------"
echo -e "${BLUE}Test 3: Local Server (if running)${NC}"
echo ""

if curl -s http://localhost:10000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Local server is running on port 10000${NC}"
    curl -s http://localhost:10000/health | python3 -m json.tool
else
    echo -e "${YELLOW}⚠ Local server not running (this is OK if you're using live deployment)${NC}"
    echo "To start local server: PORT=10000 python main.py"
fi
echo ""

echo "----------------------------------------"
echo -e "${BLUE}Test 4: MCP Server (if running)${NC}"
echo ""

if curl -s http://localhost:10001/mcp > /dev/null 2>&1; then
    echo -e "${GREEN}✓ MCP server is running on port 10001${NC}"
    echo "Status: Ready for Archestra"
else
    echo -e "${YELLOW}⚠ MCP server not running (this is OK if you're not testing Archestra)${NC}"
    echo "To start MCP server: python mcp_server.py"
fi
echo ""

echo "----------------------------------------"
echo -e "${BLUE}Test 5: Archestra Integration${NC}"
echo ""

if docker ps | grep -q archestra; then
    echo -e "${GREEN}✓ Archestra is running${NC}"
    echo "Access UI at: http://localhost:3000"
    
    if curl -s http://localhost:10001/mcp > /dev/null 2>&1; then
        echo -e "${GREEN}✓ MCP server accessible${NC}"
        echo "Archestra can connect to: http://host.docker.internal:10001/mcp"
    else
        echo -e "${YELLOW}⚠ MCP server not running - start with: python mcp_server.py${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Archestra not running (this is OK for standalone demo)${NC}"
    echo "To start Archestra: docker run -d -p 3000:3000 -p 9000:9000 archestra/platform:latest"
fi
echo ""

echo "========================================"
echo -e "${GREEN}Testing Summary${NC}"
echo "========================================"
echo ""
echo "For Demo Video:"
echo "1. ✓ Use live deployment: https://sentinel-mcp-auditor.onrender.com"
echo "2. ✓ Click all scenario buttons to show functionality"
echo "3. ✓ Take screenshots of Archestra integration (if tested)"
echo ""
echo "All systems checked!"
