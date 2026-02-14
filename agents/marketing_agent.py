"""
Marketing Agent - Simulates a marketing automation bot.
Calls LLM APIs to generate content, sometimes excessively.
"""

import time
import random
import requests
import os
from datetime import datetime

# Use localhost for local testing, host.docker.internal for Docker
AUDIT_URL = os.environ.get("AUDIT_URL", "http://localhost:10000/audit")


class MarketingAgent:
    def __init__(self, agent_id="Agent-Marketing"):
        self.agent_id = agent_id
        self.activity_log = []

    def generate_social_posts(self, count=10):
        """Generate social media posts using LLM."""
        for i in range(count):
            cost = random.uniform(0.5, 2.0)
            self.log(f"Called gpt-4 for social post generation, cost ${cost:.2f}")
            time.sleep(0.1)

    def generate_campaign_ideas(self, excessive=False):
        """Generate marketing campaign ideas."""
        count = random.randint(50, 100) if excessive else random.randint(5, 15)
        total_cost = count * random.uniform(1.0, 3.0)
        
        self.log(f"Called gpt-4 {count} times in 10 min for campaign ideas, cost ${total_cost:.2f}")
        
        if excessive:
            return "COST_SPIKE"
        return "OK"

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
    """Run marketing agent simulation."""
    agent = MarketingAgent()
    
    print(f"\n🤖 {agent.agent_id} starting...\n")
    
    # Normal operations
    agent.generate_social_posts(count=5)
    time.sleep(1)
    
    # Excessive usage (triggers cost spike)
    agent.generate_campaign_ideas(excessive=True)
    
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
