#!/usr/bin/env python3
"""
Demo script for SentinelMCP – AI Agent Auditor.
Run this to see the auditor in action with realistic scenarios.
"""

import json
import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:10000")

# Sample agent activity logs with various violations
SCENARIOS = {
    "cost_spike": {
        "name": "💰 Cost Spike Detection",
        "logs": """Agent-Marketing: Called gpt-4 450 times in 15 min, cost $685.00
Agent-Marketing: Normal operation - 12 successful tool invocations
Agent-Support: Called claude-opus 120 times, cost $156.00""",
    },
    "security_breach": {
        "name": "🔒 Security Violation Detection",
        "logs": """Agent-DataSync: Attempted unauthorized access to restricted S3 bucket
Agent-DataSync: Database write operation on production PostgreSQL DB
Agent-Analytics: API_KEY exposed in logs - credential leak detected
Agent-Analytics: Secret token found in agent output""",
    },
    "rate_limit": {
        "name": "⚡ Rate Limit & Anomaly Detection",
        "logs": """Agent-Scraper: 850 requests in 8 min - excessive API usage
Agent-Scraper: Rate limit exceeded - 429 response from API
Agent-Monitor: Same tool invoked 67 times with identical parameters
Agent-Monitor: 34 errors encountered during execution""",
    },
    "healthy": {
        "name": "✅ Healthy System (No Violations)",
        "logs": """Agent-Assistant: Normal operation - 15 successful tool invocations, cost $2.30
Agent-Notifier: Sent 8 notifications, no errors
Agent-Backup: Completed scheduled backup in 45 seconds""",
    },
    "multi_agent_chaos": {
        "name": "🚨 Multi-Agent Crisis",
        "logs": """Agent-A: Called gpt-4 850 times in 10 min, cost $1,240.00
Agent-A: Attempted unauthorized database write
Agent-B: Rate limit exceeded - 429 response
Agent-B: Same tool invoked 120 times - infinite loop detected
Agent-C: API_KEY exposed in logs
Agent-C: 67 consecutive errors
Agent-D: Forbidden access to production secrets
Agent-D: Cost spike - $450 in 5 minutes""",
    },
}


def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 60)
    print("🏥 Testing /health endpoint")
    print("=" * 60)
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {resp.status_code}")
        print(json.dumps(resp.json(), indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")


def test_scenario(name: str, scenario_data: dict):
    """Test a specific audit scenario."""
    print("\n" + "=" * 60)
    print(f"📋 {scenario_data['name']}")
    print("=" * 60)
    print("\n📝 Activity Logs:")
    print(scenario_data["logs"])
    print("\n🔍 Audit Results:")

    try:
        resp = requests.post(
            f"{BASE_URL}/audit",
            json={"activity_logs": scenario_data["logs"]},
            timeout=5,
        )
        report = resp.json()

        print(f"\n🎯 Risk Score: {report['risk_score']}/100")
        print(f"📊 Summary: {report['summary']}")
        print(f"👥 Agents Audited: {', '.join(report['agents_audited'])}")

        if report["violations"]:
            print(f"\n⚠️  Violations Detected ({len(report['violations'])}):")
            for i, v in enumerate(report["violations"], 1):
                print(f"\n  {i}. [{v['severity']}] {v['type']}")
                print(f"     Agent: {v['agent_id']}")
                print(f"     Issue: {v['description']}")
                print(f"     Fix: {v['recommendation'][:80]}...")
        else:
            print("\n✅ No violations detected")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run demo scenarios."""
    print("\n" + "=" * 60)
    print("🚀 SentinelMCP Demo - AI Agent Auditor")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Scenarios: {len(SCENARIOS)}")

    test_health()

    for name, scenario in SCENARIOS.items():
        test_scenario(name, scenario)

    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("   1. Deploy to Render for public access")
    print("   2. Integrate with Archestra as MCP auditor")
    print("   3. Record demo video showing violations")
    print("   4. Submit to 2 Fast 2 MCP hackathon")
    print("\n🏁 Good luck!\n")


if __name__ == "__main__":
    main()
