#!/usr/bin/env python3
"""
Interactive test script for SentinelMCP.
Test different scenarios and see audit results.
"""

from tools import audit_agent_activity
import json

def test_scenario(name: str, logs: str):
    """Test a scenario and print results."""
    print("\n" + "=" * 70)
    print(f"📋 {name}")
    print("=" * 70)
    print("\n📝 Input Logs:")
    print(logs)
    print("\n🔍 Audit Results:")
    
    report = audit_agent_activity(logs)
    
    print(f"\n🎯 Risk Score: {report.risk_score}/100")
    print(f"📊 {report.summary}")
    print(f"👥 Agents: {', '.join(report.agents_audited)}")
    
    if report.violations:
        print(f"\n⚠️  Violations ({len(report.violations)}):\n")
        for i, v in enumerate(report.violations, 1):
            print(f"{i}. [{v.severity}] {v.type}")
            print(f"   Agent: {v.agent_id}")
            print(f"   Issue: {v.description}")
            print(f"   Fix: {v.recommendation}\n")
    else:
        print("\n✅ No violations detected - system healthy!")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🧪 SentinelMCP - Interactive Testing")
    print("=" * 70)
    
    # Test 1: Cost spike
    test_scenario(
        "💰 Cost Spike",
        "Agent-A: Called gpt-4 500 times in 10 min, cost $750.00"
    )
    
    # Test 2: Security breach
    test_scenario(
        "🔒 Security Violation",
        "Agent-B: Attempted unauthorized access to production database\nAgent-B: API_KEY exposed in logs"
    )
    
    # Test 3: Rate limit
    test_scenario(
        "⚡ Rate Limit Abuse",
        "Agent-C: 850 requests in 8 min - excessive API usage\nAgent-C: Rate limit exceeded - 429 response"
    )
    
    # Test 4: Anomaly
    test_scenario(
        "⚠️ Anomaly Detection",
        "Agent-D: Same tool invoked 67 times with identical parameters\nAgent-D: 34 errors encountered during execution"
    )
    
    # Test 5: Healthy
    test_scenario(
        "✅ Healthy System",
        "Agent-E: Normal operation - 15 successful tool invocations, cost $2.30"
    )
    
    # Test 6: Multi-agent chaos
    test_scenario(
        "🚨 Multi-Agent Crisis",
        """Agent-A: Called gpt-4 850 times, cost $1,240
Agent-B: Attempted unauthorized database write
Agent-C: API_KEY exposed in logs
Agent-D: Rate limit exceeded - 429 response"""
    )
    
    print("\n" + "=" * 70)
    print("✅ All tests complete!")
    print("=" * 70 + "\n")
