
from uagents import Agent, Context, Protocol
from datetime import datetime, UTC
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import (
    JobParseRequest,
    JobParseResponse,
    ResumeParseRequest,
    ResumeParseResponse,
    IntersectionRequest,
    IntersectionResponse,
    DebateRequest,
    DebateResponse,
    DecisionRequest,
    DecisionResponse,
)


def create_coordinator_agent(port=8007, event_emitter=None):
    """Factory function to create a hiring coordinator agent"""

    # ALWAYS use descriptive names and unique seeds
    agent = Agent(
        name="hiring_coordinator",
        seed="coordinator_seed",
        port=port,
        endpoint=[f"http://localhost:{port}/submit"],
        mailbox=False  # Local development
    )

    # Store event emitter for real-time updates
    agent.event_emitter = event_emitter

    # Store agent addresses
    agent.job_parser_address = None
    agent.resume_parser_address = None
    agent.intersection_address = None
    agent.pro_hire_address = None
    agent.anti_hire_address = None
    agent.decision_address = None

    # Store results
    agent.job_analysis = None
    agent.resume_analysis = None
    agent.intersection_analysis = None
    agent.pro_arguments = []
    agent.anti_arguments = []
    agent.final_decision = None

    # Add completion flags
    agent.job_complete = False
    agent.resume_complete = False
    agent.intersection_complete = False
    agent.debate_complete = False
    agent.decision_complete = False

    # Add failure tracking
    agent.api_failure_count = 0
    agent.max_api_failures = 3  # Stop process after 3 API failures

    # Add flag to prevent duplicate requests
    agent.initial_requests_sent = False

    # Store initial data
    agent.resume_content = None
    agent.job_description = None
    agent.candidate_name = None
    agent.job_title = None

    # ALWAYS version your protocols
    protocol = Protocol(name="coordinator_protocol", version="1.0")

    async def _handle_api_failure_shutdown(ctx: Context):
        """Handle shutdown due to API failures"""
        print("🚨 API failure shutdown initiated")
        if agent.event_emitter:
            await agent.event_emitter(
                "System",
                "Process stopped due to API rate limit. Please try again later.",
                "error"
            )
        # Mark process as complete to prevent further execution
        agent.decision_complete = True

    async def _check_and_proceed(ctx: Context):
        """Check if we have both job and resume analysis, then proceed to intersection"""
        if agent.job_complete and agent.resume_complete:
            print(f"\n🔍 STEP 2: Evaluating Intersection")

            # Emit step transition event
            if agent.event_emitter:
                await agent.event_emitter(
                    "System", "Starting intersection evaluation", "intersection"
                )

            request = IntersectionRequest(
                job_analysis=agent.job_analysis,
                resume_analysis=agent.resume_analysis
            )
            await ctx.send(agent.intersection_address, request)

    async def _start_debate(ctx: Context):
        """Start the debate between pro and anti hire agents"""
        print(f"\n⚖️ STEP 3: Conducting Debate")

        # Emit step transition event
        if agent.event_emitter:
            await agent.event_emitter("System", "Starting debate phase", "debate")

        # Start with pro-hire argument
        pro_request = DebateRequest(
            intersection_analysis=agent.intersection_analysis,
            round_number=1
        )
        await ctx.send(agent.pro_hire_address, pro_request)

    async def _continue_debate(ctx: Context):
        """Continue the debate or end it and make decision"""
        total_rounds = len(agent.pro_arguments) + len(agent.anti_arguments)
        print(
            f"🔄 Continue debate check: Pro={len(agent.pro_arguments)}, Anti={len(agent.anti_arguments)}, Total={total_rounds}"
        )

        # Strict bounds checking to prevent extra rounds
        if (
            total_rounds < 6
            and len(agent.pro_arguments) <= 3
            and len(agent.anti_arguments) <= 3
        ):
            # Continue debate
            if len(agent.pro_arguments) > len(agent.anti_arguments):
                # Anti-hire's turn
                round_num = len(agent.anti_arguments) + 1
                previous_arg = agent.pro_arguments[-1].argument

                anti_request = DebateRequest(
                    intersection_analysis=agent.intersection_analysis,
                    round_number=round_num,
                    previous_argument=previous_arg,
                )
                await ctx.send(agent.anti_hire_address, anti_request)
            else:
                # Pro-hire's turn
                round_num = len(agent.pro_arguments) + 1
                previous_arg = (
                    agent.anti_arguments[-1].argument if agent.anti_arguments else ""
                )

                pro_request = DebateRequest(
                    intersection_analysis=agent.intersection_analysis,
                    round_number=round_num,
                    previous_argument=previous_arg,
                )
                await ctx.send(agent.pro_hire_address, pro_request)
        else:
            # Debate complete, make decision
            print(f"\n🎯 STEP 4: Making Final Decision")

            # Emit step transition event
            if agent.event_emitter:
                await agent.event_emitter(
                    "System", "Making final hiring decision", "decision"
                )

            decision_request = DecisionRequest(
                pro_arguments=agent.pro_arguments,
                anti_arguments=agent.anti_arguments,
                intersection_analysis=agent.intersection_analysis,
                candidate_name=agent.candidate_name,
                job_title=agent.job_title,
            )
            await ctx.send(agent.decision_address, decision_request)

    @agent.on_event("startup")
    async def startup(ctx: Context):
        """Agent startup handler"""
        ctx.logger.info(f"🚀 {agent.name} started successfully!")
        ctx.logger.info(f"📍 Agent address: {agent.address}")
        ctx.logger.info(f"🎯 Ready to coordinate hiring evaluation process")

    @agent.on_event("shutdown")
    async def shutdown(ctx: Context):
        """Agent shutdown handler"""
        ctx.logger.info(f"🛑 {agent.name} shutting down...")

    # Timer to send initial requests after startup
    @agent.on_interval(period=3.0)
    async def send_initial_requests(ctx: Context):
        """Send initial parsing requests when ready"""
        if (
            not agent.initial_requests_sent
            and agent.job_description
            and agent.resume_content
        ):
            print("🤖 Starting Hiring Evaluation Process")
            print("=" * 60)
            print("\n📋 STEP 1: Parsing Job and Resume")

            # Send initial requests
            job_request = JobParseRequest(
                job_description=agent.job_description,
                job_title=agent.job_title
            )
            await ctx.send(agent.job_parser_address, job_request)

            resume_request = ResumeParseRequest(
                resume_content=agent.resume_content,
                candidate_name=agent.candidate_name,
            )
            await ctx.send(agent.resume_parser_address, resume_request)

            # Mark as sent to prevent duplicates
            agent.initial_requests_sent = True

    @protocol.on_message(model=JobParseResponse)
    async def handle_job_response(ctx: Context, sender: str, msg: JobParseResponse):
        """Handle job parsing response"""
        agent.job_analysis = msg
        agent.job_complete = True
        print(f"Job Analysis: {msg.analysis}")

        # Emit WebSocket event
        if agent.event_emitter:
            await agent.event_emitter("Job Parser Agent", msg.analysis, "parsing")

        await _check_and_proceed(ctx)

    @protocol.on_message(model=ResumeParseResponse)
    async def handle_resume_response(ctx: Context, sender: str, msg: ResumeParseResponse):
        """Handle resume parsing response"""
        agent.resume_analysis = msg
        agent.resume_complete = True
        print(f"Resume Analysis: {msg.analysis}")

        # Emit WebSocket event
        if agent.event_emitter:
            await agent.event_emitter("Resume Parser Agent", msg.analysis, "parsing")

        await _check_and_proceed(ctx)

    @protocol.on_message(model=IntersectionResponse)
    async def handle_intersection_response(ctx: Context, sender: str, msg: IntersectionResponse):
        """Handle intersection evaluation response"""
        agent.intersection_analysis = msg
        agent.intersection_complete = True
        print(f"\n🔍 STEP 2: Evaluating Intersection")
        print(f"Intersection Analysis: {msg.analysis}")
        print(f"Overall Compatibility: {msg.overall_compatibility:.2f}")

        # Emit WebSocket event
        if agent.event_emitter:
            await agent.event_emitter(
                "Intersection Evaluator", msg.analysis, "evaluation", "evaluation"
            )

        await _start_debate(ctx)

    @protocol.on_message(model=DebateResponse)
    async def handle_debate_response(ctx: Context, sender: str, msg: DebateResponse):
        """Handle debate response from pro/anti hire agents"""
        # Check for API failure responses (generic fallback responses)
        if (
            msg.argument
            == "Candidate has strong technical skills and relevant experience"
        ):
            agent.api_failure_count += 1
            print(
                f"⚠️ Detected API failure response (count: {agent.api_failure_count})"
            )

            if agent.api_failure_count >= agent.max_api_failures:
                print(
                    f"🛑 Stopping process due to {agent.api_failure_count} API failures"
                )
                # Send error decision immediately
                await _handle_api_failure_shutdown(ctx)
                return

        if msg.position == "pro":
            agent.pro_arguments.append(msg)
            print(f"Pro-Hire Round {len(agent.pro_arguments)}: {msg.argument}")

            # Emit WebSocket event
            if agent.event_emitter:
                await agent.event_emitter(
                    "Pro-Hire Advocate", msg.argument, "debate", "pro"
                )
        else:
            agent.anti_arguments.append(msg)
            print(f"Anti-Hire Round {len(agent.anti_arguments)}: {msg.argument}")

            # Emit WebSocket event
            if agent.event_emitter:
                await agent.event_emitter(
                    "Anti-Hire Advocate", msg.argument, "debate", "anti"
                )

        await _continue_debate(ctx)

    @protocol.on_message(model=DecisionResponse)
    async def handle_decision_response(ctx: Context, sender: str, msg: DecisionResponse):
        """Handle final decision response"""
        agent.final_decision = msg
        print(f"\n🎯 STEP 4: Making Final Decision")
        print("\n" + "=" * 60)
        print("FINAL HIRING DECISION")
        print("=" * 60)
        print(f"Decision: {msg.decision.upper()}")
        print(f"Confidence: {msg.confidence:.2f}")
        print(f"Reasoning: {msg.reasoning}")
        print(f"Key Factors: {', '.join(msg.key_factors)}")
        print("=" * 60)

        # Emit WebSocket event
        if agent.event_emitter:
            decision_summary = f"Decision: {msg.decision.upper()}\nConfidence: {msg.confidence:.2f}\nReasoning: {msg.reasoning}"
            await agent.event_emitter(
                "Decision Agent", decision_summary, "decision", "decision"
            )

        agent.decision_complete = True

    # Include the protocol in the agent
    agent.include(protocol, publish_manifest=True)

    return agent

# Create default instance for direct use
coordinator_agent = create_coordinator_agent()


if __name__ == "__main__":
    print("""
🤖 Starting Hiring Coordinator Agent...

This agent will:
1. Orchestrate the entire hiring evaluation process
2. Coordinate communication between all agents:
   - Job Parser
   - Resume Parser
   - Intersection Evaluator
   - Pro-Hire Advocate
   - Anti-Hire Advocate
   - Decision Maker
3. Track process state and handle failures
4. Emit real-time updates via WebSocket (if configured)

🛑 Stop with Ctrl+C
    """)
    coordinator_agent.run()
