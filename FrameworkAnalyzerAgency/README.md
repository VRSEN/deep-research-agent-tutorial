# Framework Analyzer Agency

**AI agency for competitive analysis of agent orchestration frameworks - identifies missing features and technical improvements for Agency Swarm**

## 🎯 Purpose

Analyze competitor frameworks (LangGraph, CrewAI, Pydantic-AI) to identify:
- **Missing features** in Agency Swarm
- **Technical weaknesses** in competitor frameworks
- **Actionable improvements** for our codebase
- **Competitive advantages** and market positioning

## 🏢 Business Context

- **Company**: Vrsen AI Solutions - Boutique AI consultancy
- **Service**: "Agents-as-a-Service" for business automation
- **Our Framework**: Agency Swarm - Built on OpenAI Assistants API
- **Goal**: Maintain competitive advantage through data-driven improvements

## 🔧 Framework Analysis Scope

- **Agency Swarm** (Our framework) - https://github.com/VRSEN/agency-swarm
- **LangGraph** (Competitor) - https://github.com/langchain-ai/langgraph
- **CrewAI** (Competitor) - https://github.com/crewAIInc/crewAI
- **Pydantic-AI** (Competitor) - https://github.com/pydantic/pydantic-ai

## 🚀 Quick Start

### 1. Environment Setup

Create `.env` file in project root:

```bash
# Required: OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Required: GitHub Personal Access Token (create your own at https://github.com/settings/tokens)
# Note: Token only needs "public_repo" scope for reading public repositories
GITHUB_TOKEN=your_github_token_here
```

**🔑 Creating a GitHub Token:**
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select "public_repo" scope (read access to public repositories)
4. Copy the token and add it to your `.env` file

### 2. 🌐 **CRITICAL: Start ngrok for OpenAI API**

⚠️ **REQUIRED**: OpenAI API needs public URLs. **You MUST run ngrok**:

```bash
# Terminal 1: Start MCP server
cd ..  # Go to project root
python mcp/start_mcp_server.py

# Terminal 2: Start ngrok (REQUIRED for OpenAI API)
ngrok http 8001

# Copy ngrok URL (e.g., https://abc123.ngrok-free.app)
export MCP_SERVER_URL="https://your-ngrok-url.ngrok-free.app/sse"
```

**Why ngrok is required**: OpenAI API cannot access `localhost` URLs. The MCP server must be publicly accessible.

### 3. Run Framework Analysis

```bash
# Go to project root (important!)
cd /path/to/deep-research-agent-tutorial

# Set required environment variables
export GITHUB_TOKEN=your_github_token_here
export MCP_SERVER_URL="https://your-ngrok-url.ngrok-free.app/sse"

# Run the Framework Analyzer Agency
python agency.py

# Or launch Copilot UI
python agency.py --ui
```

**Important**: Always run from the project root directory, not inside the `FrameworkAnalyzerAgency/` folder.

## 📊 Analysis Features

✅ **GitHub Repository Analysis** - Uses remote GitHub MCP service
✅ **Framework Documentation** - Comprehensive LLM docs for all frameworks
✅ **No Web Search** - Focuses on authoritative code and docs
✅ **Business-Focused** - Recommendations aligned with consultancy needs
✅ **Actionable Results** - Missing features and improvement roadmap

## 🤖 Agent Workflow

1. **Triage Agent** - Determines if clarification is needed
2. **Clarifying Agent** - Asks specific questions about analysis scope
3. **Instruction Builder** - Creates detailed competitive analysis instructions
4. **Research Agent** - Performs comprehensive framework analysis

## 📈 Expected Output

- **Executive Summary** - Strategic recommendations and competitive positioning
- **Framework Comparison Matrix** - Feature and capability comparison
- **Missing Features Analysis** - What Agency Swarm should add
- **Technical Weaknesses** - Competitor framework limitations
- **Implementation Roadmap** - Prioritized recommendations

## 🔧 Technical Configuration

### GitHub MCP (Remote Service)
- **Service**: `https://api.githubcopilot.com/mcp/`
- **Authentication**: GitHub Personal Access Token
- **Analysis**: Repository structure, issues, community engagement

### File Search MCP (Local + ngrok)
- **Local Server**: `http://localhost:8001/sse`
- **Public URL**: `https://your-ngrok-url.ngrok-free.app/sse` (via ngrok)
- **Content**: Framework documentation files

## 🛠️ Troubleshooting

### ⚠️ Common Issues

**Issue**: `424 Failed Dependency` errors
**Fix**: Always use ngrok public URL: `export MCP_SERVER_URL="https://your-ngrok-url.ngrok-free.app/sse"`

**Issue**: GitHub MCP connection fails
**Fix**: Verify token: `echo $GITHUB_TOKEN`

**Issue**: MCP server not accessible
**Fix**: Test server: `curl https://your-ngrok-url.ngrok-free.app/sse`

### 🧪 Test Setup

```bash
# Test ngrok URL
curl "$MCP_SERVER_URL"

# Test simple analysis
python agency.py
# Ask: "Compare Agency Swarm vs LangGraph architecture"
```

## 📁 Project Structure

```
FrameworkAnalyzerAgency/
├── agency.py                     # Main agency entry point
├── files/                        # Framework documentation
│   ├── crewai_docs.txt          # CrewAI LLM docs
│   ├── langgraph_docs.txt       # LangGraph LLM docs
│   └── pydantic_ai_docs.txt     # Pydantic-AI LLM docs
├── ClarifyingAgent/             # Gathers analysis context
├── InstructionBuilderAgent/     # Builds analysis instructions
├── ResearchAgent/               # Performs framework analysis
└── README.md                    # This file
```

## 🎯 Key Analysis Areas

- **Architecture Patterns** - Agent structure and communication
- **Developer Experience** - Setup complexity and documentation
- **Performance** - Scalability and efficiency
- **Feature Gaps** - Missing capabilities in Agency Swarm
- **Technical Debt** - Code quality and maintainability issues
- **Market Position** - Adoption and competitive advantages

## 🔒 Security Notes

- GitHub token has read-only access to public repositories
- Uses remote GitHub MCP service
- All analysis uses publicly available information
- No sensitive data stored or transmitted

---

**🌟 Ready to analyze frameworks and improve Agency Swarm!**
