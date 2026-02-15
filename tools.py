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
# Order matters: more specific patterns first. Templates use {agent}, {count}, {cost}, {time}, {model}.
_AUDIT_RULES: list[tuple[re.Pattern[str], str, str, str, str]] = [
    # ----- Cost -----
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
        "Agent {agent} called expensive model {count}x - potential runaway costs",
        "Add rate limiting; switch to gpt-4o-mini for non-critical tasks",
    ),
    (
        re.compile(r"(Agent-\w+).*(\d+).*(\$|dollars?|usd)", re.I),
        "COST_SPIKE",
        "HIGH",
        "Agent {agent} spending (${cost}) - review for cost spike",
        "Set cost limits; monitor usage; consider cheaper models",
    ),
    (
        re.compile(r"(Agent-\w+).*(spend|spending|billing|bill|budget exceed|overrun|runaway cost)", re.I),
        "COST_SPIKE",
        "HIGH",
        "Agent {agent} cost-related activity - possible spike",
        "Review spending; set alerts; add cost caps in Archestra",
    ),
    # ----- Security -----
    (
        re.compile(r"(Agent-\w+).*(unauthorized|forbidden|denied|restricted|access denied|permission denied)", re.I),
        "SECURITY",
        "CRITICAL",
        "Agent {agent} attempted unauthorized or denied access - security policy violation",
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
        re.compile(r"(Agent-\w+).*(api[_-]?key|secret|token|password|credential|leak|leaked|exposed|breach)", re.I),
        "SECURITY",
        "CRITICAL",
        "Agent {agent} credentials/secret exposure risk - data leak possible",
        "Use Archestra secret management; rotate exposed credentials immediately",
    ),
    (
        re.compile(r"(Agent-\w+).*(admin|root|sudo|elevated|privilege escalation)", re.I),
        "SECURITY",
        "HIGH",
        "Agent {agent} elevated privilege or admin access - review scope",
        "Enforce least-privilege; audit admin actions; restrict sensitive paths",
    ),
    # ----- Rate limit -----
    (
        re.compile(r"(Agent-\w+).*(\d{3,})\s*(calls?|requests?|invocations?).*?(\d+)\s*min", re.I),
        "RATE_LIMIT",
        "HIGH",
        "Agent {agent} made {count} requests in {time} - excessive API usage",
        "Implement exponential backoff; add circuit breaker; check for infinite loops",
    ),
    (
        re.compile(r"(Agent-\w+).*(rate limit|throttle|429|503|quota exceeded|too many requests)", re.I),
        "RATE_LIMIT",
        "MEDIUM",
        "Agent {agent} hit rate limits or quota - API throttling",
        "Increase API quota or reduce request frequency; add retry logic",
    ),
    (
        re.compile(r"(Agent-\w+).*(excessive|overload|too many).*(request|call|api)", re.I),
        "RATE_LIMIT",
        "HIGH",
        "Agent {agent} excessive requests/calls - rate limit risk",
        "Add backoff; cap concurrency; monitor quota",
    ),
    (
        re.compile(r"(Agent-\w+).*(\d{3,}).*(request|call|invocation)", re.I),
        "RATE_LIMIT",
        "MEDIUM",
        "Agent {agent} high request/call volume ({count}) - monitor for limits",
        "Set rate limits; add retries; consider batching",
    ),
    # ----- Anomaly -----
    (
        re.compile(r"(Agent-\w+).*(same tool|repeated|loop|duplicate).*?(\d{2,})", re.I),
        "ANOMALY",
        "HIGH",
        "Agent {agent} called same tool {count}x - possible infinite loop",
        "Review agent logic; add loop detection; implement max iteration limits",
    ),
    (
        re.compile(r"(Agent-\w+).*(\d{2,}).*consecutive.*(error|fail)", re.I),
        "ANOMALY",
        "HIGH",
        "Agent {agent} had {count} consecutive errors - stability issue",
        "Check logs for root cause; add error handling; implement circuit breaker",
    ),
    (
        re.compile(r"(Agent-\w+).*(error|failed|exception).*(\d{2,})", re.I),
        "ANOMALY",
        "MEDIUM",
        "Agent {agent} encountered {count} errors - stability issue",
        "Check logs for root cause; add error handling; monitor agent health",
    ),
    (
        re.compile(r"(Agent-\w+).*(\d{2,}).*(error|fail|timeout|exception)", re.I),
        "ANOMALY",
        "MEDIUM",
        "Agent {agent} had {count} errors/timeouts - stability issue",
        "Check logs; add error handling; consider circuit breaker",
    ),
    (
        re.compile(r"(Agent-\w+).*(infinite loop|stuck|hang|crash|crashed|timeout|repeated failure)", re.I),
        "ANOMALY",
        "HIGH",
        "Agent {agent} stability/reliability issue - possible loop or crash",
        "Review logic; add timeouts and max retries; monitor health",
    ),
    (
        re.compile(r"(Agent-\w+).*(retry|retries).*(\d{2,})", re.I),
        "ANOMALY",
        "MEDIUM",
        "Agent {agent} high retry count ({count}) - underlying failure or overload",
        "Investigate root cause; add backoff; reduce load",
    ),
    (
        re.compile(r"(Agent-\w+).*?(\d{2,}).*(retry|retries)", re.I),
        "ANOMALY",
        "MEDIUM",
        "Agent {agent} high retry count ({count}) - underlying failure or overload",
        "Investigate root cause; add backoff; reduce load",
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
                
                # Build description with matched values (group layout varies by rule)
                count_val = "multiple"
                if match.lastindex >= 2 and "count" in desc_template:
                    if "excessive API usage" in desc_template and match.lastindex >= 4:
                        count_val = match.group(2)
                    elif "consecutive errors" in desc_template or "high request" in desc_template or "retry count" in desc_template:
                        count_val = match.group(2)
                    else:
                        count_val = match.group(3) if match.lastindex >= 3 else match.group(2)
                time_val = f"{match.group(4)} min" if match.lastindex >= 4 else "short period"
                description = desc_template.format(
                    agent=agent_id,
                    cost=match.group(2) if match.lastindex >= 2 else "unknown",
                    model=match.group(2) if "model" in desc_template else "",
                    count=count_val,
                    time=time_val,
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


# ----- Optional AI-powered audit (LLM) -----

_AUDIT_SYSTEM_PROMPT = """You are an AI agent governance auditor. Analyze activity logs from AI agents and output a JSON audit report.

Output ONLY valid JSON in this exact shape (no markdown, no extra text):
{
  "risk_score": <0-100 integer, higher = worse>,
  "violations": [
    {
      "type": "COST_SPIKE | SECURITY | RATE_LIMIT | ANOMALY",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "agent_id": "<agent name from logs>",
      "description": "<what happened>",
      "recommendation": "<how to fix>"
    }
  ],
  "summary": "<one sentence executive summary>",
  "agents_audited": ["<list of agent IDs found in logs>"]
}

Rules: Flag cost spikes ($, spending, billing), security (unauthorized access, credentials, DB writes), rate limits (429, throttle, excessive calls), anomalies (loops, errors, retries). Be precise; only report real violations. risk_score 0 if no violations."""


def audit_agent_activity_ai(activity_logs: str, api_key: str | None = None) -> AuditReport:
    """
    Audit logs using an LLM when api_key is set; otherwise fall back to rule-based.
    Use when you want the model to interpret varied or novel phrasings.
    """
    if not activity_logs or not activity_logs.strip():
        return AuditReport(
            risk_score=0,
            violations=[],
            summary="No activity logs provided for audit.",
            agents_audited=[],
        )

    api_key = api_key or __import__("os").environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return audit_agent_activity(activity_logs)

    try:
        import json
        try:
            from openai import OpenAI
        except ImportError:
            return audit_agent_activity(activity_logs)

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _AUDIT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Audit these agent activity logs:\n\n{activity_logs}"},
            ],
            temperature=0.1,
        )
        text = resp.choices[0].message.content or ""

        # Strip markdown code block if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        violations = [
            Violation(
                type=v.get("type", "ANOMALY"),
                severity=v.get("severity", "MEDIUM"),
                agent_id=v.get("agent_id", "Unknown"),
                description=v.get("description", ""),
                recommendation=v.get("recommendation", ""),
            )
            for v in data.get("violations", [])
        ]
        return AuditReport(
            risk_score=min(100, max(0, int(data.get("risk_score", 0)))),
            violations=violations,
            summary=data.get("summary", ""),
            agents_audited=list(data.get("agents_audited", [])),
        )
    except Exception:
        return audit_agent_activity(activity_logs)
