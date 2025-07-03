#!/usr/bin/env python3
"""
Deep Research Agency

Four-agent handoffs pattern with clarification workflow.
Triage → [Clarifying, Instruction] → Research using o3-deep-research model.
"""

from dotenv import load_dotenv

load_dotenv()

import os
import sys
from pathlib import Path

from agency_swarm import Agency, Agent
from ClarifyingAgent.ClarifyingAgent import ClarifyingAgent
from InstructionAgent.InstructionAgent import InstructionAgent
from ResearchAgent.ResearchAgent import ResearchAgent
from shared_outputs import Clarifications
from utils import save_research_to_pdf
from demo_utils import stream_demo, copilot_demo

# ─────────────────────────────────────────────────────────────
# Process files at application start
# ─────────────────────────────────────────────────────────────

# Get the files directory path
files_dir = Path("files")
if files_dir.exists() and files_dir.is_dir():
    print(f"📁 Found files directory with {len(list(files_dir.glob('*')))} files")
    # Files will be available through MCP server

# ─────────────────────────────────────────────────────────────
# Create agents with proper dependencies
# ─────────────────────────────────────────────────────────────

research_agent = ResearchAgent()
instruction_agent = InstructionAgent(research_agent)
clarifying_agent = ClarifyingAgent(instruction_agent)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Decide whether clarifications are required.\n"
        "• If yes → call transfer_to_clarifying_questions_agent\n"
        "• If no  → call transfer_to_research_instruction_agent\n"
        "Return exactly ONE function-call."
    ),
    handoffs=[clarifying_agent, instruction_agent],
)

# Create agency
agency = Agency(triage_agent)

# ─────────────────────────────────────────────────────────────
# Enhanced agency wrapper with automatic PDF generation
# ─────────────────────────────────────────────────────────────


def save_response_to_pdf(response, query):
    """Save response to PDF with error handling."""
    try:
        pdf_path = save_research_to_pdf(
            research_content=str(response), query=query, output_dir="reports"
        )
        print(f"\n📄 Research report saved to: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"\n❌ Error saving PDF: {e}")
        return None


def basic_research(query: str, mock_answers: dict[str, str] | None = None):
    """Run research with automatic clarification handling and PDF generation."""

    # Get initial response
    response = agency.get_response(query)

    # Handle clarification questions if they arise
    if hasattr(response, "output_type") and isinstance(
        response.output_type, Clarifications
    ):
        reply = []
        for q in response.output_type.questions:
            ans = (mock_answers or {}).get(q, "No preference.")
            reply.append(f"**{q}**\n{ans}")

        # Send clarification responses back
        response = agency.get_response("\n\n".join(reply))

    # Always save to PDF
    save_response_to_pdf(response, query)
    return response




if __name__ == "__main__":
    import asyncio
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ["--terminal", "--stream"]:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo(agency))
    else:
        print("🚀 Launching Copilot UI...")
        copilot_demo(agency, post_process=save_response_to_pdf)
