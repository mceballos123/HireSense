"""
Decision Maker Agent
===================

This agent makes the final hiring decision based on the debate between pro and anti hire advocates.
"""

from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from .models import DecisionRequest, DecisionResponse
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
            You are the final decision maker for a hiring decision. Evaluate all the arguments and make a final decision.
            
            Intersection Analysis:
            {msg.intersection_analysis.analysis}
            Overall Compatibility: {msg.intersection_analysis.overall_compatibility}
            
            Pro-Hire Arguments:
            {pro_args}
            
            Anti-Hire Arguments:
            {anti_args}
            
            Evaluate the strength of each side's arguments and make a final decision.
            Consider:
            1. Which side made stronger arguments
            2. The overall compatibility score
            3. The confidence levels of each argument
            4. The key factors that matter most for this role
            
            Respond with ONLY a JSON object in this exact format:
            {{
                "decision": "<hire/no_hire>",
                "confidence": <0.0 to 1.0>,
                "reasoning": "<detailed explanation of your decision>",
                "key_factors": ["factor1", "factor2", "factor3"]
            }}
            """

            result = await self.llm_agent.query_llm(prompt)

            if result["success"]:
                try:
                    analysis = self.llm_agent.parse_json_response(result["content"])

                    if analysis:
                        response = DecisionResponse(
                            decision=analysis.get("decision", "hire"),
                            confidence=analysis.get("confidence", 0.7),
                            reasoning=analysis.get(
                                "reasoning", "Default decision based on compatibility"
                            ),
                            key_factors=analysis.get(
                                "key_factors", ["Skills match", "Experience level"]
                            ),
                        )
                    else:
                        response = DecisionResponse(
                            decision="hire",
                            confidence=0.7,
                            reasoning="Default decision based on compatibility",
                            key_factors=["Skills match", "Experience level"],
                        )

                    print(f"🎯 {self.name}: Decision made")
                    await ctx.send(sender, response)

                except Exception as e:
                    print(f"❌ {self.name}: Error processing response: {e}")
                    response = DecisionResponse(
                        decision="hire",
                        confidence=0.7,
                        reasoning="Error processing response, using defaults",
                        key_factors=["Skills match", "Experience level"],
                    )
                    await ctx.send(sender, response)
            else:
                response = DecisionResponse(
                    decision="hire",
                    confidence=0.7,
                    reasoning="API Error, using defaults",
                    key_factors=["Skills match", "Experience level"],
                )
                await ctx.send(sender, response)

        self.include(self.protocol)
