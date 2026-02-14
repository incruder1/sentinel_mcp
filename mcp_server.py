"""
SentinelMCP - Pure MCP Server for Archestra Integration
Separate from the FastAPI REST server.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from tools import AuditReport, audit_agent_activity

# Create MCP server with relaxed security for Docker connectivity
transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,  # Disable for Docker
    allowed_hosts=["*"],  # Allow all hosts
    allowed_origins=["*"]  # Allow all origins
)

mcp = FastMCP(
    "SentinelMCP",
    transport_security=transport_security,
    host="0.0.0.0",
    port=10001
)


@mcp.tool()
def audit_agent_activity_tool(activity_logs: str) -> AuditReport:
    """
    Audit AI agent activity logs and return governance report.

    Analyzes agent activity and flags:
    - Cost violations (spending spikes)
    - Security violations (unauthorized access, credential leaks)
    - Rate limit abuse (excessive API calls)
    - Anomalies (infinite loops, repeated errors)

    Args:
        activity_logs: Raw activity logs from one or more AI agents

    Returns:
        Structured audit report with risk score, violations, and recommendations
    """
    return audit_agent_activity(activity_logs)


if __name__ == "__main__":
    # Run the MCP server
    print("Starting SentinelMCP server on 0.0.0.0:10001...")
    print("Transport security: DNS rebinding protection disabled, all hosts allowed")
    mcp.run(transport="streamable-http")
