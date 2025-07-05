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
from agents import HostedMCPTool, WebSearchTool
from agents.mcp import MCPServerSse
from dotenv import load_dotenv

from utils import run_agency_demo

load_dotenv()

# Get MCP server URL from environment or use default
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

print(f"📡 MCP Server URL: {MCP_SERVER_URL}")

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[
        WebSearchTool(),
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "file_search",
                "server_url": MCP_SERVER_URL,
                "require_approval": "never",
            }
        ),
    ],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)

if __name__ == "__main__":
    run_agency_demo(agency)
    # agency.visualize()
