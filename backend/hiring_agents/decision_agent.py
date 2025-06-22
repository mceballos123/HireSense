"""
Decision Maker Agent
===================

This agent makes the final hiring decision based on the debate between pro and anti hire advocates.
"""

from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from .models import DecisionRequest, DecisionResponse, Reasoning
from .llm_client import SimpleLLMAgent


class DecisionAgent(Agent):
    def __init__(self):
        super().__init__("decision_maker", 8006, "decision_seed")
        fund_agent_if_low(self.wallet.address())

        self.llm_agent = SimpleLLMAgent("decision_maker")
        self.protocol = Protocol()

        @self.protocol.on_message(model=DecisionRequest)
        async def handle_decision(ctx: Context, sender: str, msg: DecisionRequest):
            print(f"🎯 {self.name}: Making final hiring decision")

            # Format debate arguments for the prompt
            pro_args = "\n".join(
                [
                    f"Round {i+1}: {arg.argument}"
                    for i, arg in enumerate(msg.pro_arguments)
                ]
            )
            anti_args = "\n".join(
                [
                    f"Round {i+1}: {arg.argument}"
                    for i, arg in enumerate(msg.anti_arguments)
                ]
            )

            prompt = f"""
            You are the final decision maker for a hiring decision. Evaluate all the arguments and make a final, well-reasoned decision. Your reasoning should be comprehensive.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            
            Pro-Hire Arguments:
            {pro_args}
            
            Anti-Hire Arguments:
            {anti_args}
            
            Evaluate the strength of each side's arguments and make a final, well-reasoned decision. Your reasoning should be comprehensive.
            
            Respond with ONLY a JSON object in this exact format. The reasoning MUST be broken down into a detailed summary, and comprehensive lists of pros and cons.
            {{
                "decision": "<hire/no_hire>",
                "confidence": <0.0 to 1.0>,
                "reasoning": {{
                    "summary": "<A detailed, 2-3 sentence summary explaining the final verdict and its context.>",
                    "pros": ["<A comprehensive list of all key strengths and pro-hire arguments. Include at least 2-3 points.>", "<...more pros>"],
                    "cons": ["<A comprehensive list of all key weaknesses and anti-hire arguments. Include at least 2-3 points.>", "<...more cons>"]
                }},
                "key_factors": ["<The most important factors that drove the decision.>", "<...more factors>"]
            }}
            """

            result = await self.llm_agent.query_llm(prompt)

            if result["success"]:
                try:
                    analysis = self.llm_agent.parse_json_response(result["content"])

                    if analysis:
                        reasoning_data = analysis.get("reasoning", {})
                        response = DecisionResponse(
                            decision=analysis.get("decision", "no_hire"),
                            confidence=analysis.get("confidence", 0.7),
                            reasoning=Reasoning(
                                summary=reasoning_data.get("summary", "Analysis incomplete."),
                                pros=reasoning_data.get("pros", []),
                                cons=reasoning_data.get("cons", [])
                            ),
                            key_factors=analysis.get("key_factors", ["N/A"]),
                        )
                    else:
                        # Default response if parsing fails
                        response = DecisionResponse(
                            decision="no_hire",
                            confidence=0.0,
                            reasoning=Reasoning(
                                summary="Failed to parse LLM response.",
                                pros=[],
                                cons=["Could not generate analysis from AI."],
                            ),
                            key_factors=["Parsing Error"],
                        )

                    print(f"🎯 {self.name}: Decision made")
                    await ctx.send(sender, response)

                except Exception as e:
                    print(f"❌ {self.name}: Error processing response: {e}")
                    response = DecisionResponse(
                        decision="no_hire",
                        confidence=0.0,
                        reasoning=Reasoning(
                            summary="An exception occurred while processing the response.",
                            pros=[],
                            cons=[str(e)],
                        ),
                        key_factors=["Processing Error"],
                    )
                    await ctx.send(sender, response)
            else:
                # Default response if API call fails
                response = DecisionResponse(
                    decision="no_hire",
                    confidence=0.0,
                    reasoning=Reasoning(
                        summary="API Error.",
                        pros=[],
                        cons=[f"API Error: {result['content']}"],
                    ),
                    key_factors=["API Error"],
                )
                await ctx.send(sender, response)

        self.include(self.protocol)
