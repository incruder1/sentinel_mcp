"""
Monitor Agent - Simulates a system monitoring bot.
Checks metrics and performs health checks, sometimes getting stuck in loops.
"""

import time
import random
import requests
import os
from datetime import datetime

# Use localhost for local testing, host.docker.internal for Docker
AUDIT_URL = os.environ.get("AUDIT_URL", "http://localhost:10000/audit")


class MonitorAgent:
    def __init__(self, agent_id="Agent-Monitor"):
        self.agent_id = agent_id
        self.activity_log = []

    def check_system_health(self):
        """Check system health metrics."""
        self.log("Normal operation - system health check passed")
        time.sleep(0.1)

    def collect_metrics(self, excessive=False):
        """Collect system metrics."""
        if excessive:
            count = random.randint(80, 120)
            self.log(f"Same tool invoked {count} times with identical parameters")
            self.log(f"{random.randint(30, 50)} errors encountered during execution")
        else:
            self.log("Collected CPU, memory, disk metrics - all normal")
        time.sleep(0.1)

    def hit_rate_limit(self):
        """Hit API rate limits."""
        requests_count = random.randint(800, 900)
        self.log(f"{requests_count} requests in 8 min - excessive API usage")
        self.log("Rate limit exceeded - 429 response from API")

    def log(self, message):
        """Log activity."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {self.agent_id}: {message}"
        self.activity_log.append(log_entry)
        print(log_entry)

    def get_activity_logs(self):
        """Get all activity logs as string."""
        return "\n".join([log.split("] ", 1)[1] for log in self.activity_log])

    def send_to_auditor(self):
        """Send activity logs to SentinelMCP auditor."""
        try:
            response = requests.post(
                AUDIT_URL,
                json={"activity_logs": self.get_activity_logs()},
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"Failed to audit: {e}")
            return None


def main():
    """Run monitor agent simulation."""
    agent = MonitorAgent()
    
    print(f"\n🤖 {agent.agent_id} starting...\n")
    
    # Normal operations
    agent.check_system_health()
    time.sleep(0.5)
    
    # Anomalies
    agent.collect_metrics(excessive=True)
    time.sleep(0.5)
    agent.hit_rate_limit()
    
    print(f"\n📊 Sending activity to auditor...\n")
    audit_result = agent.send_to_auditor()
    
    if audit_result:
        print(f"Risk Score: {audit_result.get('risk_score')}/100")
        print(f"Summary: {audit_result.get('summary')}")
        if audit_result.get('violations'):
            print(f"\n⚠️  Violations: {len(audit_result['violations'])}")
            for v in audit_result['violations']:
                print(f"  - [{v['severity']}] {v['type']}: {v['description']}")


if __name__ == "__main__":
    main()
