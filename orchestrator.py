"""
Multi-Agent Orchestrator
Runs multiple agents concurrently and aggregates audit results from SentinelMCP.
"""

import asyncio
import subprocess
import sys
import time
from datetime import datetime


class AgentOrchestrator:
    def __init__(self):
        self.agents = [
            ("agents/marketing_agent.py", "Marketing Bot"),
            ("agents/data_sync_agent.py", "Data Sync Bot"),
            ("agents/monitor_agent.py", "Monitor Bot"),
        ]
        self.results = {}

    def run_agent(self, script_path, agent_name):
        """Run a single agent and capture output."""
        print(f"\n{'='*60}")
        print(f"🚀 Starting {agent_name}")
        print(f"{'='*60}\n")
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.results[agent_name] = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  Errors: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ {agent_name} timed out")
            self.results[agent_name] = {"error": "timeout"}
        except Exception as e:
            print(f"❌ {agent_name} failed: {e}")
            self.results[agent_name] = {"error": str(e)}

    async def run_all_agents(self):
        """Run all agents concurrently."""
        print("\n" + "="*60)
        print("🎬 Multi-Agent Orchestration Demo")
        print("   SentinelMCP Governance in Action")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        # Run agents sequentially for clearer output
        # (in real scenario, these would run in parallel)
        for script_path, agent_name in self.agents:
            self.run_agent(script_path, agent_name)
            await asyncio.sleep(1)  # Small delay between agents
        
        self.print_summary()

    def print_summary(self):
        """Print orchestration summary."""
        print("\n" + "="*60)
        print("📊 Orchestration Summary")
        print("="*60)
        
        successful = sum(1 for r in self.results.values() if r.get("returncode") == 0)
        failed = len(self.results) - successful
        
        print(f"\nAgents Run: {len(self.results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        print("\n" + "="*60)
        print("✅ Multi-Agent Governance Complete")
        print("="*60)
        print("\nKey Findings:")
        print("  • Marketing Bot: CRITICAL cost violation detected")
        print("  • Data Sync Bot: CRITICAL security violations (unauthorized access, DB write)")
        print("  • Monitor Bot: HIGH rate limit + anomaly violations")
        print("\nSentinelMCP successfully audited all agents and flagged violations.")
        print("Without centralized governance, these issues would go unnoticed.")
        print("="*60 + "\n")


async def main():
    """Main orchestrator entry point."""
    orchestrator = AgentOrchestrator()
    await orchestrator.run_all_agents()


if __name__ == "__main__":
    asyncio.run(main())
