"""
Intersection Evaluator Agent
===========================

This agent evaluates the intersection between job requirements and candidate profile.
"""

from uagents import Agent, Context, Protocol
# from uagents.setup import fund_agent_if_low
from .models import IntersectionRequest, IntersectionResponse
from .llm_client import SimpleLLMAgent


class IntersectionAgent(Agent):
    def __init__(self, port=8003):
        super().__init__("intersection_evaluator", port, "intersection_seed")
        # fund_agent_if_low(self.wallet.address())

        self.llm_agent = SimpleLLMAgent("intersection_evaluator")
        self.protocol = Protocol()

        @self.protocol.on_message(model=IntersectionRequest)
        async def handle_intersection(
            ctx: Context, sender: str, msg: IntersectionRequest
        ):
            print(f"🔍 {self.name}: Evaluating intersection")

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

            result = await self.llm_agent.query_llm(prompt)

            if result["success"]:
                try:
                    analysis = self.llm_agent.parse_json_response(result["content"])

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

                    print(f"🔍 {self.name}: Intersection evaluation complete")
                    await ctx.send(sender, response)

                except Exception as e:
                    print(f"❌ {self.name}: Error processing response: {e}")
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

        self.include(self.protocol)
