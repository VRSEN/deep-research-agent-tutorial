#!/usr/bin/env python3
"""
Framework Analyzer Agency

Four-agent handoffs pattern with clarification workflow.
Triage → [Clarifying, Instruction] → Research using deep research model.
Specialized for analyzing AI framework strengths, weaknesses, and competitive analysis.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Add parent directory to Python path for utils import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agency_swarm import Agency, Agent
from ClarifyingAgent.ClarifyingAgent import ClarifyingAgent
from InstructionBuilderAgent.InstructionBuilderAgent import InstructionBuilderAgent

from ResearchAgent.ResearchAgent import FrameworkResearchAgent
from utils import run_agency_demo

research_agent = FrameworkResearchAgent()
instruction_builder_agent = InstructionBuilderAgent(research_agent)
clarifying_agent = ClarifyingAgent(instruction_builder_agent)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Decide whether clarifications are required for framework analysis.\n"
        "• If yes → call transfer_to_clarifying_questions_agent\n"
        "• If no  → call transfer_to_research_instruction_agent\n"
        "Return exactly ONE function-call."
    ),
    handoffs=[clarifying_agent, instruction_builder_agent],
)

agency = Agency(triage_agent)

if __name__ == "__main__":
    run_agency_demo(agency)
