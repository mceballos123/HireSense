
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import DebateRequest, DebateResponse

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from backend.helper_func.llm_client import SimpleLLMAgent

def create_pro_hire_agent(port=8004):
    """Factory function to create a pro-hire advocate agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="pro_hire_advocate",
        seed="pro_hire_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Initialize LLM client
    llm_agent = SimpleLLMAgent("pro_hire_advocate")

    # ALWAYS version your protocols
    protocol = Protocol(name="pro_hire_protocol", version="1.0")

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"✅ Ready to build pro-hire arguments")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    @protocol.on_message(model=DebateRequest, replies=DebateResponse)
    async def handle_debate(ctx: Context, sender: str, msg: DebateRequest):
        """Handle incoming debate requests and build pro-hire arguments"""
        ctx.logger.info(
            f"✅ {agent.name}: Building pro-hire argument (round {msg.round_number})"
        )

        prompt = f"""
        You are a pro-hire advocate. Build a compelling argument for hiring this candidate.

        Intersection Analysis:
        {msg.intersection_analysis.analysis}
        Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
        Skill Matches: {', '.join(msg.intersection_analysis.skill_matches)}
        Skill Gaps: {', '.join(msg.intersection_analysis.skill_gaps)}

        Previous Anti-Hire Argument: {msg.previous_argument}

        Build a strong pro-hire argument for round {msg.round_number}.
        Focus on the candidate's strengths and how they outweigh any concerns.

        Respond with ONLY a JSON object in this exact format:
        {{
            "argument": "<your pro-hire argument>",
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
                        position="pro",
                        argument=analysis.get(
                            "argument",
                            "Candidate has strong technical skills and relevant experience",
                        ),
                        confidence=analysis.get("confidence", 0.8),
                        key_points=analysis.get(
                            "key_points", ["Technical skills", "Experience level"]
                        ),
                    )
                else:
                    response = DebateResponse(
                        position="pro",
                        argument="Candidate has strong technical skills and relevant experience",
                        confidence=0.8,
                        key_points=["Technical skills", "Experience level"],
                    )

                ctx.logger.info(f"✅ {agent.name}: Pro-hire argument complete")
                await ctx.send(sender, response)

            except Exception as e:
                ctx.logger.error(f"❌ {agent.name}: Error processing response: {e}")
                response = DebateResponse(
                    position="pro",
                    argument="Candidate has strong technical skills and relevant experience",
                    confidence=0.8,
                    key_points=["Technical skills", "Experience level"],
                )
                await ctx.send(sender, response)
        else:
            response = DebateResponse(
                position="pro",
                argument="Candidate has strong technical skills and relevant experience",
                confidence=0.8,
                key_points=["Technical skills", "Experience level"],
            )
            await ctx.send(sender, response)

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent

# Create default instance for direct use
pro_hire_agent = create_pro_hire_agent()


if __name__ == "__main__":
    print("""
🤖 Starting Pro-Hire Advocate Agent...

This agent will:
1. Listen for debate requests from the coordinator
2. Build compelling pro-hire arguments based on candidate analysis
3. Respond with structured arguments including confidence and key points

🛑 Stop with Ctrl+C
    """)
    pro_hire_agent.run()
