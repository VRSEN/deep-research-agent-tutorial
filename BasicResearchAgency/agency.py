#!/usr/bin/env python3
"""
Basic Research Agency

Single agent with o4-mini-deep-research model.
Using Agency Swarm v1.x with proper streaming pattern.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agency_swarm import Agency, Agent
from agents import WebSearchTool
from demo_utils import stream_demo, copilot_demo

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[WebSearchTool()],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)


if __name__ == "__main__":
    import asyncio
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ["--terminal", "--stream"]:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo(agency))
    else:
        print("🚀 Launching Copilot UI...")
        copilot_demo(agency)
