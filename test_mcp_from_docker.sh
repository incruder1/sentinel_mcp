#!/bin/bash
# Test MCP server connectivity from within Archestra container

echo "=== Testing MCP Server from Archestra Container ==="
echo ""
echo "1. Testing DNS resolution:"
docker exec archestra sh -c "getent hosts host.docker.internal"
echo ""

echo "2. Testing TCP connectivity to port 10001:"
docker exec archestra sh -c "nc -zv host.docker.internal 10001 2>&1"
echo ""

echo "3. Testing HTTP GET to /mcp:"
docker exec archestra sh -c "wget -O- --timeout=5 http://host.docker.internal:10001/mcp 2>&1 | head -20"
echo ""

echo "4. Testing HTTP POST to /mcp (simulating MCP handshake):"
docker exec archestra sh -c 'wget -O- --timeout=5 --post-data="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\"}" --header="Content-Type: application/json" http://host.docker.internal:10001/mcp 2>&1 | head -20'
