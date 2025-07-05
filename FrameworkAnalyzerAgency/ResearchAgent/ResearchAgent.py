import os

from agency_swarm import Agent
from agents import HostedMCPTool
from agents.mcp.server import MCPServerSse


class FrameworkResearchAgent(Agent):
    def __init__(self):
        # Get MCP server URL from environment or use default
        mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

        # Get GitHub token from environment (required for GitHub MCP server)
        github_token = os.getenv("GITHUB_TOKEN")

        # Configure GitHub MCP server (remote) - only if token is provided
        mcp_servers = []
        if github_token:
            github_mcp_server = MCPServerSse(
                {
                    "url": "https://api.githubcopilot.com/mcp/",
                    "headers": {"Authorization": f"Bearer {github_token}"},
                    "timeout": 10,  # connect timeout (seconds)
                    "sse_read_timeout": 300,  # idle-read timeout (seconds)
                },
                cache_tools_list=True,  # avoids an RTT on every run
            )
            mcp_servers.append(github_mcp_server)

        super().__init__(
            name="Framework Research Agent",
            model="o4-mini-deep-research-2025-06-26",
            instructions="Perform comprehensive framework analysis based on the user's instructions.",
            tools=[
                # Internal file search MCP server for local document analysis
                HostedMCPTool(
                    tool_config={
                        "type": "mcp",
                        "server_label": "file_search",
                        "server_url": mcp_server_url,
                        "require_approval": "never",
                    }
                ),
            ],
            mcp_servers=mcp_servers,  # Remote MCP servers (GitHub if token provided)
        )
