
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import sys
import os
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import JobParseRequest, JobParseResponse

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from backend.helper_func.llm_client import SimpleLLMAgent


def create_job_parser_agent(port=8001):
    """Factory function to create a job parser agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="job_parser",
        seed="job_parser_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Initialize LLM client
    llm_agent = SimpleLLMAgent("job_parser")

    # ALWAYS version your protocols
    protocol = Protocol(name="job_parser_protocol", version="1.0")

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"💼 Ready to parse job descriptions")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    @protocol.on_message(model=JobParseRequest, replies=JobParseResponse)
    async def handle_job_parse(ctx: Context, sender: str, msg: JobParseRequest):
        """Handle incoming job parsing requests"""
        ctx.logger.info(f"💼 {agent.name}: Parsing job description for {msg.job_title}")

        prompt = f"""
        Analyze the following job description and extract key information.

        Job Title: {msg.job_title}
        Job Description:
        {msg.job_description}

        Extract and analyze:
        1. Required skills (must-have technical skills)
        2. Preferred skills (nice-to-have skills)
        3. Experience level (Junior, Mid-level, Senior)
        4. Key requirements and responsibilities

        Respond with ONLY a JSON object in this exact format:
        {{
            "required_skills": ["skill1", "skill2"],
            "preferred_skills": ["skill3", "skill4"],
            "experience_level": "<Junior/Mid-level/Senior>",
            "key_requirements": ["req1", "req2"],
            "analysis": "<brief analysis of the job requirements>"
        }}
        """

        result = await llm_agent.query_llm(prompt)

        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])

                if analysis:
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=analysis.get(
                            "required_skills", ["python", "javascript"]
                        ),
                        preferred_skills=analysis.get(
                            "preferred_skills", ["react"]
                        ),
                        experience_level=analysis.get(
                            "experience_level", "Mid-level"
                        ),
                        key_requirements=analysis.get(
                            "key_requirements", ["web development"]
                        ),
                        analysis=analysis.get("analysis", "Job analysis completed"),
                    )
                else:
                    response = JobParseResponse(
                        job_title=msg.job_title,
                        required_skills=["python", "javascript"],
                        preferred_skills=["react"],
                        experience_level="Mid-level",
                        key_requirements=["web development"],
                        analysis="Failed to parse LLM response, using defaults",
                    )

                ctx.logger.info(f"💼 {agent.name}: Job parsing complete")
                await ctx.send(sender, response)

            except Exception as e:
                ctx.logger.error(f"❌ {agent.name}: Error processing response: {e}")
                response = JobParseResponse(
                    job_title=msg.job_title,
                    required_skills=["python", "javascript"],
                    preferred_skills=["react"],
                    experience_level="Mid-level",
                    key_requirements=["web development"],
                    analysis="Error processing response, using defaults",
                )
                await ctx.send(sender, response)
        else:
            response = JobParseResponse(
                job_title=msg.job_title,
                required_skills=["python", "javascript"],
                preferred_skills=["react"],
                experience_level="Mid-level",
                key_requirements=["web development"],
                analysis=f"API Error: {result['content']}",
            )
            await ctx.send(sender, response)

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent

# Create default instance for direct use
job_parser_agent = create_job_parser_agent()


if __name__ == "__main__":
    print("""
🤖 Starting Job Parser Agent...

This agent will:
1. Listen for job parsing requests from the coordinator
2. Analyze job descriptions using LLM
3. Extract required/preferred skills, experience level, and key requirements
4. Return structured job analysis

🛑 Stop with Ctrl+C
    """)
    job_parser_agent.run()
