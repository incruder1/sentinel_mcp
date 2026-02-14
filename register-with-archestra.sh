#!/bin/bash
# Register SentinelMCP with Archestra via API

AUTH_TOKEN="NEzEq4X1MjpTOKCvcWZADv7tQJbsYXmU2hF6McOyPkIscHbtRiKaIr3YkyF3kxVg"
ARCHESTRA_API="http://localhost:9000/api/v1"

# Register MCP Server
echo "Registering SentinelMCP with Archestra..."

curl -X POST "$ARCHESTRA_API/mcp/servers" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sentinel-mcp-auditor",
    "description": "AI Agent Auditor - Meta-level governance for multi-agent systems",
    "url": "http://host.docker.internal:10000",
    "transport": "http",
    "capabilities": {
      "tools": true,
      "resources": false,
      "prompts": false
    },
    "metadata": {
      "author": "devjohri",
      "repository": "https://github.com/incruder1/sentinel_mcp",
      "tags": ["governance", "security", "cost-control", "observability"]
    }
  }'

echo ""
echo "Registration attempt complete. Check Archestra UI."
