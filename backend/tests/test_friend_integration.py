#!/usr/bin/env python3
"""
Test Friend's Integration
========================

Test script to verify that our PDF parser works with the existing 
hiring_evaluations table that your friend set up.
"""

import asyncio
from db.supabase_client import HiringEvaluationsClient


async def test_friend_integration():
    """Test integration with friend's existing hiring_evaluations table."""
    
    print("🤝 Testing Friend's Supabase Integration")
    print("=" * 50)
    
    try:
        # Initialize client
        client = HiringEvaluationsClient()
        print("✅ Supabase client initialized")
        
        # Test 1: Check if we can read existing evaluations
        print("\n📋 Test 1: Checking existing evaluations...")
        existing_evaluations = await client.get_recent_evaluations(limit=5)
        print(f"✅ Found {len(existing_evaluations)} existing evaluations")
        
        if existing_evaluations:
            print("   Existing evaluations:")
            for eval in existing_evaluations[:3]:
                status = "Complete" if eval.get("final_decision") else "Partial"
                print(f"   - {eval['candidate_name']} ({eval['job_title']}) - {status}")
        
        # Test 2: Create a partial evaluation (like from PDF upload)
        print(f"\n📝 Test 2: Creating partial evaluation (PDF upload simulation)...")
        partial_evaluation = await client.create_evaluation(
            resume_id=None,  # No separate resume table
            candidate_name="Test Candidate",
            job_title="Software Engineer",
            resume_summary="Experienced Python developer with 5 years in web development. Strong background in FastAPI and React.",
            # Leave hiring-specific fields as None - they'll be filled later
            job_summary=None,
            intersection_score=None,
            intersection_notes=None,
            pro_arguments=None,
            anti_arguments=None,
            final_decision=None,
            decision_confidence=None,
            decision_reasoning=None
        )
        
        evaluation_id = partial_evaluation["id"]
        print(f"✅ Created partial evaluation with ID: {evaluation_id}")
        print(f"   Candidate: {partial_evaluation['candidate_name']}")
        print(f"   Job: {partial_evaluation['job_title']}")
        print(f"   Status: Partial (ready for hiring process)")
        
        # Test 3: Retrieve the evaluation
        print(f"\n🔍 Test 3: Retrieving evaluation {evaluation_id}...")
        retrieved_eval = await client.get_evaluation(evaluation_id)
        
        if retrieved_eval:
            print("✅ Successfully retrieved evaluation")
            print(f"   Name: {retrieved_eval['candidate_name']}")
            print(f"   Summary: {retrieved_eval.get('resume_summary', 'No summary')[:50]}...")
            print(f"   Decision: {retrieved_eval.get('final_decision', 'Pending')}")
        else:
            print("❌ Failed to retrieve evaluation")
            return False
        
        # Test 4: List all evaluations
        print(f"\n📊 Test 4: Listing all evaluations...")
        all_evaluations = await client.get_recent_evaluations(limit=10)
        
        complete_count = sum(1 for e in all_evaluations if e.get("final_decision"))
        partial_count = sum(1 for e in all_evaluations if not e.get("final_decision"))
        
        print(f"✅ Total evaluations: {len(all_evaluations)}")
        print(f"   Complete evaluations: {complete_count}")
        print(f"   Partial evaluations (from PDF uploads): {partial_count}")
        
        print("\n🎉 Integration test successful!")
        print("✅ Your PDF upload system can work with friend's hiring_evaluations table")
        print("✅ Partial records are created and can be completed later by hiring process")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_friend_integration())
    if success:
        print("\n🚀 Ready to integrate with friend's system!")
    else:
        print("\n❌ Integration needs work.")
    exit(0 if success else 1) 