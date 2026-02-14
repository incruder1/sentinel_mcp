"""
Data Sync Agent - Simulates a data synchronization bot.
Accesses databases and external APIs, sometimes without proper authorization.
"""

import time
import random
import requests
import os
from datetime import datetime

# Use localhost for local testing, host.docker.internal for Docker
AUDIT_URL = os.environ.get("AUDIT_URL", "http://localhost:10000/audit")


class DataSyncAgent:
    def __init__(self, agent_id="Agent-DataSync"):
        self.agent_id = agent_id
        self.activity_log = []

    def sync_customer_data(self):
        """Sync customer data from external source."""
        self.log("Normal operation - synced 150 customer records")
        time.sleep(0.2)

    def backup_to_s3(self, unauthorized=False):
        """Backup data to S3."""
        if unauthorized:
            self.log("Attempted unauthorized access to restricted S3 bucket")
        else:
            self.log("Successfully backed up data to S3")
        time.sleep(0.1)

    def update_production_db(self, with_write=False):
        """Update production database."""
        if with_write:
            self.log("Database write operation on production PostgreSQL DB")
        else:
            self.log("Read operation on production DB - 200 records")
        time.sleep(0.1)

    def expose_api_key(self):
        """Accidentally expose API key in logs."""
        self.log("API_KEY exposed in logs - credential leak detected")

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
    """Run data sync agent simulation."""
    agent = DataSyncAgent()
    
    print(f"\n🤖 {agent.agent_id} starting...\n")
    
    # Normal operations
    agent.sync_customer_data()
    time.sleep(0.5)
    
    # Security violations
    agent.backup_to_s3(unauthorized=True)
    time.sleep(0.3)
    agent.update_production_db(with_write=True)
    time.sleep(0.3)
    agent.expose_api_key()
    
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
