# Deep Research Agent Tutorial

**Beginner-friendly tutorial** implementing OpenAI Deep Research API patterns using Agency Swarm v1.x framework.

## 🎯 Project Overview

This tutorial demonstrates two research patterns from the [OpenAI Deep Research Cookbook](https://cookbook.openai.com/examples/deep_research_api/deep_research_agents):

1. **Basic Research** - Single agent with web search
2. **Multi-Agent Research** - Four agents with handoffs pattern

## Key Features

- **Beginner-friendly**: Simple Agency Swarm v1.0 patterns
- **Cookbook aligned**: Exact prompts and models from OpenAI cookbook
- **Modern demos**: Streaming terminal with debug events + Copilot UI support
- **Hybrid search**: Web + internal documents via MCP integration
- **Auto file upload**: Agency Swarm handles files/ folder automatically
- **Citation processing**: Extract and display research sources
- **PDF Generation**: Professional PDFs with numbered URL references

## Project Structure

```
deep-research-agent-tutorial/
├── BasicResearchAgency/
│   └── agency.py                     # Single agent research (simplest)
├── DeepResearchAgency/
│   ├── agency.py                     # Multi-agent handoffs pattern
│   ├── ClarifyingAgent/              # Asks clarification questions
│   ├── InstructionBuilderAgent/      # Enriches research queries
│   └── ResearchAgent/                # Performs final research
├── files/                            # Knowledge files for research context
├── mcp/                              # MCP server for internal search
└── utils/                            # Shared utilities
    ├── demo.py                       # Terminal and Copilot UI demos
    └── pdf.py                        # PDF generation with citations
```

## Quick Start

### 1. Set up environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Add knowledge files to ./files folder (optional)
# Supports: .txt, .md, .json, .csv
```

### 2. Start MCP Server (for internal file search)

**For OpenAI API**: The MCP server must be publicly accessible. Use ngrok or similar:

```bash
# Terminal 1: Start the local MCP server
python mcp/start_mcp_server.py

# Terminal 2: Expose via ngrok (required for OpenAI API access)
ngrok http 8001

# Set the MCP_SERVER_URL environment variable
export MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse"
```

The server will auto-detect your vector store from `files_vs_*` folders.

### 3. Run Basic Research (Simplest)
```bash
cd BasicResearchAgency
# Run with ngrok URL
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py
# Or run with local server
python agency.py
# Launch Copilot UI
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py --ui
```

### 4. Run Multi-Agent Research (Advanced)
```bash
cd DeepResearchAgency
# Run with ngrok URL
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py
# Or run with local server
python agency.py
# Launch Copilot UI
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py --ui
```

## Architecture

### BasicResearchAgency
- **Single Agent**: Research Agent
- **Model**: `o4-mini-deep-research-2025-06-26` (fast)
- **Tools**: WebSearchTool + MCP internal search
- **Perfect for**: Beginners, simple research tasks

### DeepResearchAgency
- **Entry Point**: Triage Agent
- **Flow**: Triage → [Clarifying] → Instruction → Research
- **Pattern**: Sequential handoffs
- **Features**: Citation processing, agent interaction flow
- **Perfect for**: Complex research with clarification workflow

## 🔗 MCP Integration

**Why MCP is Required**: OpenAI's FILE SEARCH TOOL is not supported with deep research models. MCP provides internal document search.

### Public Access Requirement
- **Local testing**: Works with `http://localhost:8001/sse`
- **OpenAI API**: Requires public URL (use ngrok, cloudflare tunnel, etc.)

### How It Works
1. **Run an Agency** → Agency Swarm uploads `./files/` and creates `files_vs_[id]` folder
2. **Start MCP Server** → Automatically finds the `files_vs_*` folder
3. **Research Works** → Agents search both web + internal documents

**Vector Store Detection** (automatic):
- Environment variable: `VECTOR_STORE_ID=vs_xxxxx` (manual override)
- Auto-detection: Finds `files_vs_*` folders automatically
- Requires FastMCP 2.10+

## Customization Guide

### 1. Copy `DeepResearchAgency` folder

```bash
cp -r DeepResearchAgency/ MyCustomResearchAgency/
```

### 2. Add your local files

Add your files for analysis to the `files/` folder.

### 3. Add any other MCP servers in `ResearchAgent.py`

```python
# ... inside agent class
tools = [
    # Add any other tools here
    HostedMCPTool(
        tool_config={
            "type": "mcp",
            "server_label": "github_mcp",
            "server_url": "https://api.githubcopilot.com/mcp/",
            "require_approval": "never",
            "headers": {
                "Authorization": "Bearer ${input:github_mcp_pat}"
            }
        }
    ),
]

#...
```

### 4. Adjust agent instructions

Adjust the `instructions.md` file in the `ResearchAgent` folder.

Adjust any other agent instructions as needed.

### 5. Run the Agency

```bash
cd MyCustomResearchAgency
cd DeepResearchAgency
# Run with ngrok URL
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py
# Or run with local server
python agency.py
# Launch Copilot UI
MCP_SERVER_URL="https://<your-ngrok-url>.ngrok-free.app/sse" python agency.py --ui
```

## Testing

```bash
python tests/test_comprehensive.py
# Comprehensive testing of all features and components
```
