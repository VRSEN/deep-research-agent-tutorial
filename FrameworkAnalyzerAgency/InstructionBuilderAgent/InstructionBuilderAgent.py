import os

from agency_swarm import Agent


class InstructionBuilderAgent(Agent):
    def __init__(self, research_agent):
        # Load instruction from file
        instructions_path = os.path.join(os.path.dirname(__file__), "instructions.md")
        with open(instructions_path, "r", encoding="utf-8") as f:
            instructions = f.read()

        super().__init__(
            name="Framework Analysis Instruction Builder",
            model="gpt-4.1",
            temperature=0,
            instructions=instructions,
            handoffs=[research_agent],
        )
