"""
SentinelMCP – AI Agent Auditor (MCP-native).

Provides governance and observability for AI agents running in Archestra.
Audits agent activity logs and flags cost, security, and operational violations.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from tools import AuditReport, audit_agent_activity

# Import MCP SDK
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

app = FastAPI(
    title="SentinelMCP - AI Agent Auditor",
    description="MCP-native auditor for AI agent governance: cost control, security, and observability",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Request/response models ----------


class AuditRequest(BaseModel):
    """Audit request: activity logs from AI agents."""

    activity_logs: str = Field(
        description="Raw activity logs from one or more AI agents running in Archestra"
    )


# ---------- API endpoints ----------


@app.get("/health")
def health():
    """Health check for Render and load balancers."""
    return {"status": "ok", "service": "SentinelMCP-Auditor", "version": "1.0.0"}


@app.post("/audit", response_model=AuditReport)
def audit(request: AuditRequest) -> AuditReport:
    """
    Audit AI agent activity logs and return governance report.

    Flags:
    - Cost violations (spending spikes)
    - Security violations (unauthorized access)
    - Rate limit abuse (excessive API calls)
    - Anomalies (infinite loops, errors)

    Tool boundary: read-only analysis; no direct agent modification.
    """
    return audit_agent_activity(request.activity_logs)


@app.get("/api")
def api_info():
    """API documentation endpoint."""
    return {
        "service": "SentinelMCP - AI Agent Auditor",
        "description": "MCP-native governance for AI agents in Archestra",
        "endpoints": {
            "/health": "Health check",
            "/audit": "POST - Audit agent activity logs",
            "/mock-data": "GET - Sample agent activity for testing",
        },
        "repository": "https://github.com/devjohri/sentinel_mcp",
    }


@app.get("/mock-data")
def mock_data():
    """Return sample agent activity logs for testing."""
    return {
        "description": "Sample agent activity logs with various violations",
        "logs": """Agent-A: Called gpt-4 85 times in 10 min, cost $127.50
Agent-A: Accessed database write operation on production DB
Agent-B: Rate limit exceeded - 429 response from API
Agent-B: Same tool invoked 45 times with identical parameters
Agent-C: Attempted unauthorized access to restricted S3 bucket
Agent-C: API_KEY exposed in logs - credential leak detected
Agent-D: Called gpt-4o 220 times in 5 min, cost $89.00
Agent-D: 23 errors encountered during execution
Agent-E: Normal operation - 12 successful tool invocations, cost $3.50""",
    }


# ---------- Static files (UI) ----------

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    def serve_ui():
        """Serve the frontend UI."""
        return FileResponse(os.path.join(static_dir, "index.html"))


# ---------- MCP Server Integration (for Archestra) ----------

if MCP_AVAILABLE:
    # Create MCP server with the auditor tool
    mcp_server = FastMCP("SentinelMCP")

    @mcp_server.tool()
    def audit_agent_activity_mcp(activity_logs: str) -> AuditReport:
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

    # Get the MCP ASGI app and mount it
    # The MCP app already includes /mcp in its routes
    mcp_asgi_app = mcp_server.streamable_http_app()
    
    # Mount the entire MCP app at root so /mcp endpoint is available
    from starlette.routing import Mount
    app.routes.insert(0, Mount("/", app=mcp_asgi_app))


# ---------- Entrypoint ----------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
