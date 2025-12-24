
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import DebateRequest, DebateResponse

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from helper_func.llm_client import SimpleLLMAgent


def create_anti_hire_agent(port=8005):
    """Factory function to create an anti-hire advocate agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="anti_hire_advocate",
        seed="anti_hire_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Initialize LLM client
    llm_agent = SimpleLLMAgent("anti_hire_advocate")

    # ALWAYS version your protocols
    protocol = Protocol(name="anti_hire_protocol", version="1.0")

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"❌ Ready to build anti-hire arguments")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    @protocol.on_message(model=DebateRequest, replies=DebateResponse)
    async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
        """Handle incoming debate requests and build anti-hire arguments"""
        ctx.logger.info(
            f"❌ {agent.name}: Building anti-hire argument (round {msg.round_number})"
        )

        prompt = f"""
        You are an anti-hire advocate. Build a compelling argument against hiring this candidate.

        Intersection Analysis:
        {msg.intersection_analysis.analysis}
        Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
        Skill Matches: {', '.join(msg.intersection_analysis.skill_matches)}
        Skill Gaps: {', '.join(msg.intersection_analysis.skill_gaps)}

        Previous Pro-Hire Argument: {msg.previous_argument}

        Build a strong anti-hire argument for round {msg.round_number}.
        Focus on the candidate's weaknesses and potential risks.

        Respond with ONLY a JSON object in this exact format:
        {{
            "argument": "<your anti-hire argument>",
            "confidence": <0.0 to 1.0>,
            "key_points": ["point1", "point2", "point3"]
        }}
        """

        result = await llm_agent.query_llm(prompt)

        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])

                if analysis:
                    response = DebateResponse(
                        position="anti",
                        argument=analysis.get(
                            "argument", "Candidate has significant skill gaps"
                        ),
                        confidence=analysis.get("confidence", 0.6),
                        key_points=analysis.get(
                            "key_points", ["Missing skills", "Experience concerns"]
                        ),
                    )
                else:
                    response = DebateResponse(
                        position="anti",
                        argument="Candidate has significant skill gaps",
                        confidence=0.6,
                        key_points=["Missing skills", "Experience concerns"],
                    )

                ctx.logger.info(f"❌ {agent.name}: Anti-hire argument complete")
                await ctx.send(sender, response)

            except Exception as e:
                ctx.logger.error(f"❌ {agent.name}: Error processing response: {e}")
                response = DebateResponse(
                    position="anti",
                    argument="Candidate has significant skill gaps",
                    confidence=0.6,
                    key_points=["Missing skills", "Experience concerns"],
                )
                await ctx.send(sender, response)
        else:
            response = DebateResponse(
                position="anti",
                argument="Candidate has significant skill gaps",
                confidence=0.6,
                key_points=["Missing skills", "Experience concerns"],
            )
            await ctx.send(sender, response)

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent

# Create default instance for direct use
anti_hire_agent = create_anti_hire_agent()


if __name__ == "__main__":
    anti_hire_agent.run()
