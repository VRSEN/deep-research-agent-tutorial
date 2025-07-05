import os

from agency_swarm import Agent
from agents import HostedMCPTool, WebSearchTool


class FrameworkResearchAgent(Agent):
    def __init__(self):
        # Get MCP server URL from environment or use default
        mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

        super().__init__(
            name="Framework Research Agent",
            model="o4-mini-deep-research-2025-06-26",
            instructions="Perform comprehensive framework analysis based on the user's instructions.",
            tools=[
                # Internal file search MCP server for local document analysis
                WebSearchTool(),
                HostedMCPTool(
                    tool_config={
                        "type": "mcp",
                        "server_label": "file_search",
                        "server_url": mcp_server_url,
                        "require_approval": "never",
                    }
                )
            ]
        )
