
from uagents import Agent, Context, Protocol
# from uagents.setup import fund_agent_if_low  # Disabled to avoid network calls
from .models import JobParseRequest, JobParseResponse
from .llm_client import SimpleLLMAgent
import json


class JobParserAgent(Agent):
    def __init__(self, port=8001):
        super().__init__("job_parser", port, "job_parser_seed")
        # fund_agent_if_low(self.wallet.address())  # Disabled for local operation

        self.llm_agent = SimpleLLMAgent("job_parser")
        self.protocol = Protocol()

        @self.protocol.on_message(model=JobParseRequest)
        async def handle_job_parse(ctx: Context, sender: str, msg: JobParseRequest):
            print(f"💼 {self.name}: Parsing job description for {msg.job_title}")

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

            result = await self.llm_agent.query_llm(prompt)

            if result["success"]:
                try:
                    analysis = self.llm_agent.parse_json_response(result["content"])

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

                    print(f"💼 {self.name}: Job parsing complete")
                    await ctx.send(sender, response)

                except Exception as e:
                    print(f"❌ {self.name}: Error processing response: {e}")
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

        self.include(self.protocol)
