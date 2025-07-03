"""Shared demo utilities for Agency Swarm examples."""

from __future__ import annotations

import asyncio
import sys
from typing import Callable, Optional

from agency_swarm import Agency
from DeepResearchAgency.shared_outputs import Clarifications
from DeepResearchAgency.utils import save_research_to_pdf


async def stream_response(agency: Agency, message: str) -> str:
    """Stream a response from the agency with basic progress output."""
    print(f"\n🔥 Streaming: {message}")
    print("⏳ Research in progress...\n")
    print("📡 Response: ", end="", flush=True)

    full_text = ""
    async for event in agency.get_response_stream(message):
        if hasattr(event, "data"):
            data = event.data
            if hasattr(data, "delta") and hasattr(data, "type") and data.type == "response.output_text.delta":
                delta_text = data.delta
                if delta_text:
                    print(delta_text, end="", flush=True)
                    full_text += delta_text
        elif isinstance(event, dict):
            event_type = event.get("event", event.get("type"))
            if event_type == "error":
                print(f"\n❌ Error: {event.get('content', event.get('data', 'Unknown error'))}")
                break

    print("\n✅ Stream complete")
    print(f"📋 Total: {len(full_text)} characters streamed")
    return full_text


async def _single_agent_stream_demo(agency: Agency) -> None:
    print("🌟 Basic Research Agency - Deep Research Tool")
    print("=" * 50)
    print("Ask any research question. Type 'quit' to exit.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            if not query:
                print("Please enter a research question.")
                continue
            await stream_response(agency, query)
            print("\n" + "=" * 50)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def _multi_agent_stream_demo(agency: Agency) -> None:
    print("🎯 Deep Research Agency - Advanced Multi-Agent Research")
    print("Multi-agent workflow: Triage → [Clarifying] → Instruction → Research")
    print("=" * 70)
    print("Ask any research question. Type 'quit' to exit.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            if not query:
                print("Please enter a research question.")
                continue

            current_agent = agency.root_agent.name
            research_content = ""
            clarification_questions = []
            awaiting_clarifications = False

            print(f"\n🤖 Starting with {current_agent}...")
            print("─" * 50)

            async for event in agency.get_response_stream(query):
                if hasattr(event, "type") and event.type == "agent_updated_stream_event" and hasattr(event, "new_agent"):
                    current_agent = event.new_agent.name
                    print(f"\n\n🔄 Switched to: {current_agent}")
                    print("─" * 50)
                    if current_agent == "Research Agent":
                        print("🔬 Performing deep research... This may take a few minutes.")
                elif hasattr(event, "data"):
                    data = event.data
                    if hasattr(data, "delta") and hasattr(data, "type") and data.type == "response.output_text.delta":
                        delta_text = data.delta or ""
                        if current_agent != "Clarifying Questions Agent":
                            print(delta_text, end="", flush=True)
                        if current_agent == "Research Agent":
                            research_content += delta_text
                        if current_agent == "Clarifying Questions Agent":
                            clarification_questions.append(delta_text)
                elif hasattr(event, "item") and isinstance(event.item, Clarifications):
                    clarification_questions = event.item.questions
                    awaiting_clarifications = True
                elif isinstance(event, dict) and event.get("event") == "error":
                    print(f"\n❌ Error: {event.get('content', event.get('data'))}")
                    break

            if awaiting_clarifications and clarification_questions:
                print("\n\n" + "─" * 50)
                print("✏️ Please answer the following questions:\n")
                answers = []
                for q in clarification_questions:
                    ans = input(f"{q}\n   Your answer: ").strip() or "No preference."
                    answers.append(f"**{q}**\n{ans}")
                print("\n🔄 Processing your answers...")
                print("─" * 50)
                async for event in agency.get_response_stream("\n\n".join(answers)):
                    if hasattr(event, "data"):
                        data = event.data
                        if hasattr(data, "delta") and hasattr(data, "type") and data.type == "response.output_text.delta":
                            delta_text = data.delta or ""
                            print(delta_text, end="", flush=True)
                            research_content += delta_text

            if research_content.strip():
                print("\n\n" + "─" * 50)
                save_research_to_pdf(research_content, query)
            else:
                print("\n\n⚠️ No research content generated. PDF not saved.")

            print("\n" + "=" * 70)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


async def stream_demo(agency: Agency) -> None:
    """Interactive terminal demo handling single or multi-agent workflows."""
    if agency.root_agent.name == "Triage Agent":
        await _multi_agent_stream_demo(agency)
    else:
        await _single_agent_stream_demo(agency)


def copilot_demo(agency: Agency, post_process: Optional[Callable[[str, str], None]] = None) -> None:
    """Launch Copilot UI. Optionally run post_process(result, query) after each response."""
    try:
        from agency_swarm.ui.demos.launcher import CopilotDemoLauncher

        if post_process:
            class WrapperAgency(Agency):
                def get_response(self, query: str, **kwargs):
                    response = super().get_response(query, **kwargs)
                    post_process(str(response), query)
                    return response

            agency = WrapperAgency(agency.root_agent)

        launcher = CopilotDemoLauncher()
        launcher.start(agency)
    except ImportError:
        print("❌ Copilot demo requires additional dependencies")
        print("Install with: pip install agency-swarm[copilot]")
