#!/usr/bin/env python3
"""
Test Supabase Integration
=========================

Test script to validate that the PDF parser output structure 
matches the Supabase database schema.
"""

import asyncio
import json
from db.supabase_client import HiringEvaluationsClient


async def test_supabase_integration():
    """Test the Supabase integration with sample data."""
    
    print("🧪 Testing Supabase Integration")
    print("=" * 50)
    
    try:
        # Initialize client
        client = HiringEvaluationsClient()
        print("✅ Supabase client initialized")
        
        # Test 1: Create a sample resume
        print("\n📝 Test 1: Creating sample resume...")
        resume_data = await client.create_resume(
            candidate_name="John Doe",
            resume_text="Sample resume text with Python, JavaScript, and React experience. 5 years of software development.",
            original_filename="john_doe_resume.pdf",
            skills=["Python", "JavaScript", "React", "FastAPI"],
            experience_years=5,
            experience_level="Mid-level",
            key_achievements=["Led team of 3 developers", "Increased system performance by 40%"],
            analysis_summary="Strong full-stack developer with 5 years experience"
        )
        
        resume_id = resume_data["id"]
        print(f"✅ Created resume with ID: {resume_id}")
        print(f"   Candidate: {resume_data['candidate_name']}")
        print(f"   Skills: {resume_data['skills']}")
        
        # Test 2: Retrieve the resume
        print(f"\n🔍 Test 2: Retrieving resume {resume_id}...")
        retrieved_resume = await client.get_resume(resume_id)
        
        if retrieved_resume:
            print("✅ Successfully retrieved resume")
            print(f"   Name: {retrieved_resume['candidate_name']}")
            print(f"   Experience: {retrieved_resume['experience_level']}")
            print(f"   Text length: {retrieved_resume['text_length']}")
        else:
            print("❌ Failed to retrieve resume")
            return False
        
        # Test 3: Search resumes
        print(f"\n🔎 Test 3: Searching resumes...")
        search_results = await client.search_resumes(
            skills=["Python"],
            experience_level="Mid-level",
            min_years=3
        )
        
        print(f"✅ Found {len(search_results)} matching resumes")
        for result in search_results:
            print(f"   - {result['candidate_name']} ({result['experience_level']})")
        
        # Test 4: Create hiring evaluation
        print(f"\n📊 Test 4: Creating hiring evaluation...")
        evaluation_data = await client.create_evaluation(
            resume_id=resume_id,
            candidate_name="John Doe",
            job_title="Senior Python Developer",
            resume_summary="Experienced full-stack developer",
            job_summary="Looking for senior Python developer with React experience",
            intersection_score=0.85,
            intersection_notes="Strong match for technical skills",
            pro_arguments=[
                {"argument": "Strong Python experience", "weight": 0.9},
                {"argument": "React experience matches job requirements", "weight": 0.8}
            ],
            anti_arguments=[
                {"argument": "Might need more senior-level experience", "weight": 0.3}
            ],
            final_decision="HIRE",
            decision_confidence=0.82,
            decision_reasoning="Strong technical match with good experience level"
        )
        
        evaluation_id = evaluation_data["id"]
        print(f"✅ Created evaluation with ID: {evaluation_id}")
        print(f"   Decision: {evaluation_data['final_decision']}")
        print(f"   Confidence: {evaluation_data['decision_confidence']}")
        
        # Test 5: Get recent resumes
        print(f"\n📋 Test 5: Getting recent resumes...")
        recent_resumes = await client.get_recent_resumes(limit=5)
        print(f"✅ Retrieved {len(recent_resumes)} recent resumes")
        
        print("\n🎉 All tests passed! Supabase integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_supabase_integration())
    exit(0 if success else 1) 