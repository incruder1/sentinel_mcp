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

from tools import AuditReport, audit_agent_activity, audit_agent_activity_ai

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
    use_ai: bool = Field(default=False, description="Use LLM for audit (set OPENAI_API_KEY); else rule-based")


# ---------- API endpoints ----------


@app.get("/health")
def health():
    """Health check for Render and load balancers."""
    return {"status": "ok", "service": "SentinelMCP-Auditor", "version": "1.0.0"}


@app.post("/audit", response_model=AuditReport)
def audit(request: AuditRequest) -> AuditReport:
    """
    Audit AI agent activity logs and return governance report.

    Use use_ai=true to analyze with an LLM (handles varied phrasings; requires OPENAI_API_KEY).
    Default is fast rule-based audit (no API key).
    """
    if request.use_ai:
        return audit_agent_activity_ai(request.activity_logs)
    return audit_agent_activity(request.activity_logs)


@app.get("/api")
def api_info():
    """API documentation endpoint."""
    return {
        "service": "SentinelMCP - AI Agent Auditor",
        "description": "MCP-native governance for AI agents in Archestra",
        "endpoints": {
            "/health": "Health check",
            "/audit": "POST - Audit logs (body: activity_logs, use_ai?); use_ai=true = LLM (OPENAI_API_KEY)",
            "/mock-data": "GET - Sample agent activity for testing",
        },
        "repository": "https://github.com/incruder1/sentinel_mcp",
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


# MCP server for Archestra runs separately: python mcp_server.py
# Do not mount MCP here or it overrides / and /health on Render.


# ---------- Entrypoint ----------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
