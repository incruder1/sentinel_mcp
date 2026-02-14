# Live Demo Script for SentinelMCP

## **2-3 Minute Demo Plan**

---

## **Opening (15 seconds)**
"Hi, I'm presenting SentinelMCP - an AI Agent Auditor that provides governance and security for multi-agent systems. This solves a critical problem: as organizations deploy more AI agents, they need a way to monitor costs, security, and compliance."

---

## **Part 1: Standalone Demo (60 seconds)**

### Show Live Deployment
1. Open: https://sentinel-mcp-auditor.onrender.com
2. "Here's SentinelMCP running live on Render."

### Demonstrate Core Features
3. **Click "Cost Spike"**
   - "Let's test a cost violation scenario"
   - Point to risk score appearing
   - Highlight the violation details
   - "Notice it detected the spending spike and provided recommendations"

4. **Click "Security Breach"**
   - "Now let's check security violations"
   - Show the HIGH severity flag
   - Point to specific violation: "It caught unauthorized admin access and credential exposure"

5. **Click "Multi-Agent Crisis"**
   - "Here's a complex scenario with multiple agents having issues"
   - Show risk score: 85 (critical)
   - "It identified problems across all three agents and prioritized them"

---

## **Part 2: Archestra Integration (45 seconds)**

### Show Integration Proof
6. **Open Archestra UI screenshot** (or show live if you have API key)
   - "SentinelMCP is fully integrated with Archestra.AI via MCP protocol"
   - Show: "Successfully installed sentinel-mcp-auditor"
   - Point to the tool being discovered

7. **Explain the Architecture**
   - "It works in two modes:"
   - "Standalone REST API for direct integration"
   - "MCP server for orchestration platforms like Archestra"
   - "This makes it flexible for any multi-agent setup"

### Show Technical Implementation (if showing terminal)
8. **Quick code glimpse** (optional)
   - Show `mcp_server.py`
   - "Built using FastMCP with proper protocol compliance"
   - Show MCP server logs: "You can see the successful connections and tool discovery"

---

## **Part 3: Real-World Value (30 seconds)**

### Business Impact
9. "Why does this matter?"
   - **Cost Control**: "Catches spending spikes before they blow your budget"
   - **Security**: "Detects credential leaks and unauthorized access in real-time"
   - **Compliance**: "Provides audit trails for AI agent activity"
   - **Governance**: "Central oversight for distributed agent systems"

### Future Vision
10. "This is just the start:"
    - "Can extend to real-time monitoring dashboards"
    - "Policy enforcement across agent networks"
    - "Integration with incident response systems"

---

## **Closing (15 seconds)**
11. "SentinelMCP is production-ready, open source, and designed for the emerging need of AI agent governance. Check it out at the GitHub link in the submission. Thank you!"

---

## **Key Points to Emphasize**

✅ **Working Live Deployment** - Not just a demo, actually running in production  
✅ **Real MCP Integration** - Not theoretical, actually connected to Archestra  
✅ **Solves Real Problem** - Cost, security, compliance for multi-agent systems  
✅ **Production Ready** - Clean UI, error handling, proper architecture  
✅ **Extensible** - Can add more tools and integrate with other platforms  

---

## **Demo URLs Quick Reference**

- **Live App:** https://sentinel-mcp-auditor.onrender.com
- **GitHub:** https://github.com/devjohri/sentinel_mcp
- **Health Check:** https://sentinel-mcp-auditor.onrender.com/health
- **API Docs:** https://sentinel-mcp-auditor.onrender.com/api

---

## **Backup Points (If Asked Questions)**

**Q: How does it detect violations?**
A: Pattern matching on agent logs with predefined rules for cost spikes, security issues, rate limits, and anomalies. Calculates risk scores based on severity and frequency.

**Q: Can it work with any agent framework?**
A: Yes! Works via REST API or MCP protocol. Any agent that can make HTTP requests or use MCP can be audited.

**Q: Is it scalable?**
A: Absolutely. Stateless design, can be deployed to cloud, handles concurrent requests, and MCP integration allows orchestration at scale.

**Q: What about false positives?**
A: Rules are configurable and can be tuned. The system provides context with each violation so teams can adjust thresholds.

---

## **Recording Tips**

1. **Test everything before recording** - Click all buttons to make sure server is warm
2. **Have browser tabs ready** - Live app, Archestra screenshot, GitHub
3. **Practice once** - Time yourself, aim for 2:30-2:45
4. **Show enthusiasm** - You built something cool and working!
5. **Clear audio** - Use good mic, quiet room
6. **Screen resolution** - 1920x1080 or 1280x720, high contrast

---

## **Screen Recording Setup**

### Recommended Layout
- **Primary screen:** Live demo at https://sentinel-mcp-auditor.onrender.com
- **Secondary tabs ready:**
  - Archestra UI (localhost:3000 with server installed)
  - GitHub repo
  - Terminal with MCP server logs (optional)

### What to Record
- Start with live app, full screen
- Use browser's full screen mode (F11 or Cmd+Shift+F)
- Keep mouse movements smooth and deliberate
- Zoom in if needed for specific details

---

## **If Time is Short (90 Second Version)**

1. **Show live app** (30s)
   - Open URL
   - Click 2-3 scenarios
   - Show results

2. **Mention Archestra** (20s)
   - "Fully integrated via MCP"
   - Show screenshot quickly

3. **Explain value** (25s)
   - Cost, security, compliance
   - Production ready

4. **Close** (15s)
   - GitHub link
   - Thank you

---

Good luck with your demo! 🚀
