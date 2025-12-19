
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import ResumeParseRequest, ResumeParseResponse

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from backend.helper_func.llm_client import SimpleLLMAgent


def create_resume_parser_agent(port=8002):
    """Factory function to create a resume parser agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="resume_parser",
        seed="resume_parser_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Initialize LLM client
    llm_agent = SimpleLLMAgent("resume_parser")

    # ALWAYS version your protocols
    protocol = Protocol(name="resume_parser_protocol", version="1.0")

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"📄 Ready to parse resumes")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    @protocol.on_message(model=ResumeParseRequest, replies=ResumeParseResponse)
    async def handle_resume_parse(ctx: Context, sender: str, msg: ResumeParseRequest):
        """Handle incoming resume parsing requests"""
        ctx.logger.info(f"📄 {agent.name}: Parsing resume for {msg.candidate_name}")

        # The content and rules for the LLM (Protocol)
        prompt = f"""
        Analyze the following resume and extract key information.

        Candidate Name: {msg.candidate_name}
        Resume Content:
        {msg.resume_content}

        Extract and analyze:
        1. Technical skills (programming languages, frameworks, tools)
        2. Years of experience
        3. Experience level (Junior, Mid-level, Senior)
        4. Key achievements and accomplishments

        Respond with ONLY a JSON object in this exact format:
        {{
            "skills": ["skill1", "skill2", "skill3"],
            "experience_years": <number>,
            "experience_level": "<Junior/Mid-level/Senior>",
            "key_achievements": ["achievement1", "achievement2"],
            "analysis": "<brief analysis of the candidate's profile>"
        }}
        """

        result = await llm_agent.query_llm(prompt)

        if result["success"]:
            try:
                analysis = llm_agent.parse_json_response(result["content"])

                if analysis:
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=analysis.get(
                            "skills", ["python", "javascript", "react"]
                        ),
                        experience_years=analysis.get("experience_years", 3),
                        experience_level=analysis.get(
                            "experience_level", "Mid-level"
                        ),
                        key_achievements=analysis.get(
                            "key_achievements", ["Led development team"]
                        ),
                        analysis=analysis.get(
                            "analysis", "Resume analysis completed"
                        ),
                    )
                else:
                    response = ResumeParseResponse(
                        candidate_name=msg.candidate_name,
                        skills=["python", "javascript", "react"],
                        experience_years=3,
                        experience_level="Mid-level",
                        key_achievements=["Led development team"],
                        analysis="Failed to parse LLM response, using defaults",
                    )

                ctx.logger.info(f"📄 {agent.name}: Resume parsing complete")
                await ctx.send(sender, response)

            except Exception as e:
                ctx.logger.error(f"❌ {agent.name}: Error processing response: {e}")
                response = ResumeParseResponse(
                    candidate_name=msg.candidate_name,
                    skills=["python", "javascript", "react"],
                    experience_years=3,
                    experience_level="Mid-level",
                    key_achievements=["Led development team"],
                    analysis="Error processing response, using defaults",
                )
                await ctx.send(sender, response)
        else:
            response = ResumeParseResponse(
                candidate_name=msg.candidate_name,
                skills=["python", "javascript", "react"],
                experience_years=3,
                experience_level="Mid-level",
                key_achievements=["Led development team"],
                analysis=f"API Error: {result['content']}",
            )
            await ctx.send(sender, response)

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent


# For backward compatibility with old class-based imports
class ResumeParserAgent:
    """Backward compatibility wrapper for class-based imports"""
    def __new__(cls, port=8002):
        return create_resume_parser_agent(port)


# Create default instance for direct use
resume_parser_agent = create_resume_parser_agent()


if __name__ == "__main__":
    print("""
🤖 Starting Resume Parser Agent...

This agent will:
1. Listen for resume parsing requests from the coordinator
2. Analyze resume content using LLM
3. Extract technical skills, experience level, and achievements
4. Return structured resume analysis

🛑 Stop with Ctrl+C
    """)
    resume_parser_agent.run()
