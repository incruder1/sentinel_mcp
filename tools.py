"""
SentinelMCP – AI Agent Auditor (MCP-native).

Audits activity logs from AI agents running in Archestra and flags:
- Cost violations (spending spikes)
- Security violations (unauthorized access)
- Rate limit abuse (excessive tool calls)
- Anomalies (infinite loops, unusual patterns)

Tool boundary: accepts only string input (agent activity logs), returns structured
audit report. Read-only; no direct agent modification.
"""

import re
from datetime import datetime
from pydantic import BaseModel, Field


class Violation(BaseModel):
    """Single violation detected in agent activity."""

    type: str = Field(description="COST_SPIKE | SECURITY | RATE_LIMIT | ANOMALY")
    severity: str = Field(description="CRITICAL | HIGH | MEDIUM | LOW")
    agent_id: str = Field(description="Agent that triggered the violation")
    description: str = Field(description="What happened")
    recommendation: str = Field(description="How to fix it")


class AuditReport(BaseModel):
    """Structured audit report for AI agent governance."""

    risk_score: int = Field(description="Overall risk score (0-100, higher = worse)")
    violations: list[Violation] = Field(default_factory=list, description="Detected violations")
    summary: str = Field(description="Executive summary of audit findings")
    agents_audited: list[str] = Field(default_factory=list, description="Agent IDs included in audit")


# Audit rules: (pattern, violation_type, severity, description_template, recommendation)
_AUDIT_RULES: list[tuple[re.Pattern[str], str, str, str, str]] = [
    # Cost violations
    (
        re.compile(r"(Agent-\w+).*cost.*\$(\d+)", re.I),
        "COST_SPIKE",
        "CRITICAL",
        "Agent {agent} incurred ${cost} in charges - exceeds threshold",
        "Set cost limits in Archestra; review agent prompt efficiency; consider cheaper models",
    ),
    (
        re.compile(r"(Agent-\w+).*(gpt-4|claude-opus|o1).*(\d{2,})\s*calls?", re.I),
        "COST_SPIKE",
        "HIGH",
        "Agent {agent} called expensive model {model} {count}x - potential runaway costs",
        "Add rate limiting; switch to gpt-4o-mini for non-critical tasks",
    ),
    # Security violations
    (
        re.compile(r"(Agent-\w+).*(unauthorized|forbidden|denied|restricted)", re.I),
        "SECURITY",
        "CRITICAL",
        "Agent {agent} attempted unauthorized access - security policy violation",
        "Review agent permissions in Archestra; enforce least-privilege access",
    ),
    (
        re.compile(r"(Agent-\w+).*(database|db|sql|postgres|mysql|redis).*write", re.I),
        "SECURITY",
        "HIGH",
        "Agent {agent} performed database write - elevated privilege usage",
        "Restrict write permissions; require approval workflow for DB modifications",
    ),
    (
        re.compile(r"(Agent-\w+).*(api[_-]?key|secret|token|password|credential)", re.I),
        "SECURITY",
        "CRITICAL",
        "Agent {agent} accessed sensitive credentials - data leak risk",
        "Use Archestra secret management; rotate exposed credentials immediately",
    ),
    # Rate limit violations
    (
        re.compile(r"(Agent-\w+).*(\d{3,})\s*(calls?|requests?|invocations?).*(\d+)\s*min", re.I),
        "RATE_LIMIT",
        "HIGH",
        "Agent {agent} made {count} requests in {time} - excessive API usage",
        "Implement exponential backoff; add circuit breaker; check for infinite loops",
    ),
    (
        re.compile(r"(Agent-\w+).*(rate limit|throttle|429|quota exceeded)", re.I),
        "RATE_LIMIT",
        "MEDIUM",
        "Agent {agent} hit rate limits - API quota exceeded",
        "Increase API quota or reduce request frequency; add retry logic",
    ),
    # Anomaly detection
    (
        re.compile(r"(Agent-\w+).*(same tool|repeated|loop|duplicate).*(\d{2,})", re.I),
        "ANOMALY",
        "HIGH",
        "Agent {agent} called same tool {count}x - possible infinite loop",
        "Review agent logic; add loop detection; implement max iteration limits",
    ),
    (
        re.compile(r"(Agent-\w+).*(error|failed|exception).*(\d{2,})", re.I),
        "ANOMALY",
        "MEDIUM",
        "Agent {agent} encountered {count} errors - stability issue",
        "Check logs for root cause; add error handling; monitor agent health",
    ),
]


def audit_agent_activity(activity_logs: str) -> AuditReport:
    """
    Audit AI agent activity logs and return structured governance report.

    Tool contract: read-only. Accepts activity logs as string; no side effects.
    Designed for MCP-based multi-agent governance under Archestra.

    Args:
        activity_logs: Raw activity logs from one or more AI agents

    Returns:
        AuditReport with risk score, violations, and recommendations
    """
    if not activity_logs or not activity_logs.strip():
        return AuditReport(
            risk_score=0,
            violations=[],
            summary="No activity logs provided for audit.",
            agents_audited=[],
        )

    lines = [line.strip() for line in activity_logs.strip().splitlines() if line.strip()]
    violations: list[Violation] = []
    agents_seen: set[str] = set()

    for line in lines:
        # Extract agent ID from line
        agent_match = re.search(r"Agent-\w+", line)
        if agent_match:
            agents_seen.add(agent_match.group(0))

        # Check each audit rule
        for pattern, violation_type, severity, desc_template, recommendation in _AUDIT_RULES:
            match = pattern.search(line)
            if match:
                # Extract dynamic values from match
                agent_id = match.group(1) if match.lastindex >= 1 else "Unknown"
                
                # Build description with matched values
                description = desc_template.format(
                    agent=agent_id,
                    cost=match.group(2) if match.lastindex >= 2 else "unknown",
                    model=match.group(2) if "model" in desc_template else "",
                    count=match.group(3) if match.lastindex >= 3 and "count" in desc_template else match.group(2) if match.lastindex >= 2 and "count" in desc_template else "multiple",
                    time=f"{match.group(4)} min" if match.lastindex >= 4 else "short period",
                )

                violations.append(
                    Violation(
                        type=violation_type,
                        severity=severity,
                        agent_id=agent_id,
                        description=description,
                        recommendation=recommendation,
                    )
                )
                break  # One violation per line

    # Calculate risk score
    risk_score = min(100, len(violations) * 15 + sum(
        35 if v.severity == "CRITICAL" else 25 if v.severity == "HIGH" else 15 if v.severity == "MEDIUM" else 5
        for v in violations
    ))

    # Generate summary
    if not violations:
        summary = f"✅ No violations detected. Audited {len(agents_seen)} agent(s). System healthy."
    else:
        critical = sum(1 for v in violations if v.severity == "CRITICAL")
        high = sum(1 for v in violations if v.severity == "HIGH")
        summary = (
            f"⚠️ {len(violations)} violation(s) detected across {len(agents_seen)} agent(s). "
            f"{critical} CRITICAL, {high} HIGH. Immediate action required."
        )

    return AuditReport(
        risk_score=risk_score,
        violations=violations,
        summary=summary,
        agents_audited=sorted(list(agents_seen)),
    )
