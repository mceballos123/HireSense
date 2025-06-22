"""
Main Entry Point for uAgents Hiring System
==========================================

This file runs the complete hiring system with all uAgents organized in separate files.
"""

import asyncio
from hiring_agents import (
    JobParserAgent,
    ResumeParserAgent,
    IntersectionAgent,
    ProHireAgent,
    AntiHireAgent,
    DecisionAgent,
    HiringCoordinator,
)
from db.supabase_client import HiringEvaluationsClient


async def run_hiring_system(
    resume_content: str, job_description: str, candidate_name: str, job_title: str
):
    """Run the complete hiring system with uAgents"""
    print("🚀 Starting uAgents Hiring System")
    print("=" * 60)

    # Create all agents
    job_parser = JobParserAgent()
    resume_parser = ResumeParserAgent()
    intersection_evaluator = IntersectionAgent()
    pro_hire = ProHireAgent()
    anti_hire = AntiHireAgent()
    decision_maker = DecisionAgent()
    coordinator = HiringCoordinator()

    # Start all agents in background tasks
    job_parser_task = asyncio.create_task(job_parser.run_async())
    resume_parser_task = asyncio.create_task(resume_parser.run_async())
    intersection_task = asyncio.create_task(intersection_evaluator.run_async())
    pro_hire_task = asyncio.create_task(pro_hire.run_async())
    anti_hire_task = asyncio.create_task(anti_hire.run_async())
    decision_task = asyncio.create_task(decision_maker.run_async())
    coordinator_task = asyncio.create_task(coordinator.run_async())

    # Wait for initialization
    print("⏳ Waiting for agents to initialize...")
    await asyncio.sleep(5)

    # Store addresses
    coordinator.job_parser_address = job_parser.address
    coordinator.resume_parser_address = resume_parser.address
    coordinator.intersection_address = intersection_evaluator.address
    coordinator.pro_hire_address = pro_hire.address
    coordinator.anti_hire_address = anti_hire.address
    coordinator.decision_address = decision_maker.address

    # Store initial data
    coordinator.resume_content = resume_content
    coordinator.job_description = job_description
    coordinator.candidate_name = candidate_name
    coordinator.job_title = job_title

    # Wait for decision to complete
    print("⏳ Waiting for hiring process to complete...")
    while not coordinator.decision_complete:
        await asyncio.sleep(1)

    # Cancel all tasks
    job_parser_task.cancel()
    resume_parser_task.cancel()
    intersection_task.cancel()
    pro_hire_task.cancel()
    anti_hire_task.cancel()
    decision_task.cancel()
    coordinator_task.cancel()

    print("\n✅ Hiring evaluation completed!")

    # Save evaluation to Supabase
    supabase_client = HiringEvaluationsClient()
    # Wait for the coordinator to have all the data
    await supabase_client.create_evaluation(
        candidate_name=coordinator.candidate_name,
        job_title=coordinator.job_title,
        resume_summary=(
            coordinator.resume_analysis.analysis
            if coordinator.resume_analysis
            else None
        ),
        job_summary=(
            coordinator.job_analysis.analysis if coordinator.job_analysis else None
        ),
        intersection_score=(
            coordinator.intersection_analysis.overall_compatibility
            if coordinator.intersection_analysis
            else None
        ),
        intersection_notes=(
            coordinator.intersection_analysis.analysis
            if coordinator.intersection_analysis
            else None
        ),
        pro_arguments=[arg.model_dump() for arg in coordinator.pro_arguments],
        anti_arguments=[arg.model_dump() for arg in coordinator.anti_arguments],
        final_decision=(
            coordinator.decision_complete and "HIRE"
            if getattr(coordinator, "final_decision", "HIRE") == "HIRE"
            else "REJECT"
        ),
        decision_confidence=getattr(coordinator, "decision_confidence", None),
        decision_reasoning=getattr(coordinator, "decision_reasoning", None),
    )
    print("✅ Evaluation saved to Supabase!")


# Test data and main execution
if __name__ == "__main__":
    # Test data
    resume_content = """
    Software Engineer with 3 years of experience in web development.
    Proficient in Python, JavaScript, React, and Node.js.
    Experience with MongoDB and AWS services.
    Led development of multiple production applications.
    Strong problem-solving skills and experience with agile methodologies.
    """

    job_description = """
    Mid-level Software Engineer position.
    Required skills: Python, JavaScript, React.
    Preferred skills: Node.js, MongoDB, AWS.
    Experience with microservices and cloud deployment preferred.
    Looking for someone with 2-5 years of experience.
    """

    # Run the hiring system
    asyncio.run(
        run_hiring_system(
            resume_content=resume_content,
            job_description=job_description,
            candidate_name="John Doe",
            job_title="Software Engineer",
        )
    )
