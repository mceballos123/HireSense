
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import IntersectionRequest, IntersectionResponse

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from backend.helper_func.llm_client import SimpleLLMAgent


def create_intersection_agent(port=8003):
    """Factory function to create an intersection evaluation agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="intersection_evaluator",
        seed="intersection_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Initialize LLM client
    llm_agent = SimpleLLMAgent("intersection_evaluator")

    # ALWAYS version your protocols
    protocol = Protocol(name="intersection_protocol", version="1.0")

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"🔍 Ready to evaluate job-candidate intersections")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    @protocol.on_message(model=IntersectionRequest, replies=IntersectionResponse)
    async def handle_intersection(ctx: Context, sender: str, msg: IntersectionRequest):
        """Handle incoming intersection evaluation requests"""
        ctx.logger.info(f"🔍 {agent.name}: Evaluating intersection")

        prompt = f"""
        Evaluate the intersection between job requirements and candidate profile.

        Job Analysis:
        {msg.job_analysis.analysis}
        Required Skills: {', '.join(msg.job_analysis.required_skills)}
        Preferred Skills: {', '.join(msg.job_analysis.preferred_skills)}
        Experience Level: {msg.job_analysis.experience_level}

        Resume Analysis:
        {msg.resume_analysis.analysis}
        Skills: {', '.join(msg.resume_analysis.skills)}
        Experience: {msg.resume_analysis.experience_years} years ({msg.resume_analysis.experience_level})

        Evaluate:
        1. Skill matches and gaps
        2. Experience level compatibility
        3. Overall compatibility score (0.0 to 1.0)

        Respond with ONLY a JSON object in this exact format:
        {{
            "analysis": "<detailed analysis of the intersection>",
            "overall_compatibility": <0.0 to 1.0>,
            "skill_matches": ["match1", "match2"],
            "skill_gaps": ["gap1", "gap2"],
            "experience_match": "<excellent/good/fair/poor>"
        }}
        """

        result = await llm_agent.query_llm(prompt)

        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])

                if analysis:
                    response = IntersectionResponse(
                        analysis=analysis.get(
                            "analysis", "Intersection analysis completed"
                        ),
                        overall_compatibility=analysis.get(
                            "overall_compatibility", 0.7
                        ),
                        skill_matches=analysis.get(
                            "skill_matches", ["python", "javascript"]
                        ),
                        skill_gaps=analysis.get("skill_gaps", ["microservices"]),
                        experience_match=analysis.get("experience_match", "good"),
                    )
                else:
                    response = IntersectionResponse(
                        analysis="Default intersection analysis",
                        overall_compatibility=0.7,
                        skill_matches=["python", "javascript"],
                        skill_gaps=["microservices"],
                        experience_match="good",
                    )

                ctx.logger.info(f"🔍 {agent.name}: Intersection evaluation complete")
                await ctx.send(sender, response)

            except Exception as e:
                ctx.logger.error(f"❌ {agent.name}: Error processing response: {e}")
                response = IntersectionResponse(
                    analysis="Error processing response, using defaults",
                    overall_compatibility=0.7,
                    skill_matches=["python", "javascript"],
                    skill_gaps=["microservices"],
                    experience_match="good",
                )
                await ctx.send(sender, response)
        else:
            response = IntersectionResponse(
                analysis=f"API Error: {result['content']}",
                overall_compatibility=0.7,
                skill_matches=["python", "javascript"],
                skill_gaps=["microservices"],
                experience_match="good",
            )
            await ctx.send(sender, response)

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent

# Create default instance for direct use
intersection_agent = create_intersection_agent()


if __name__ == "__main__":
    print("""
🤖 Starting Intersection Evaluator Agent...

This agent will:
1. Listen for intersection evaluation requests from the coordinator
2. Analyze compatibility between job requirements and candidate profiles
3. Identify skill matches and gaps
4. Calculate overall compatibility scores
5. Assess experience level alignment

🛑 Stop with Ctrl+C
    """)
    intersection_agent.run()
