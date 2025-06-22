"""
Supabase Client for Hiring Evaluations
======================================

This module provides a client to interact with the hiring_evaluations table in Supabase.
"""

SUPABASE_URL = "https://tceiqtjpxoqeaykptdrj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjZWlxdGpweG9xZWF5a3B0ZHJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1NTkwMDYsImV4cCI6MjA2NjEzNTAwNn0.7UNQCNuPagUG8Q0CJ9U0woUTamJu3B3PwM2JEuUBpfE"

import os
from typing import Dict, List, Optional, Any
from supabase import create_client, Client
from datetime import datetime
import json


class HiringEvaluationsClient:
    """Client for managing hiring evaluations in Supabase"""

    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        """
        Initialize the Supabase client

        Args:
            supabase_url: Supabase project URL (defaults to SUPABASE_URL env var)
            supabase_key: Supabase anon key (defaults to SUPABASE_KEY env var)
        """
        self.supabase_url = supabase_url or SUPABASE_URL
        self.supabase_key = supabase_key or SUPABASE_KEY

        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase URL and key must be provided or set as environment variables"
            )

        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    async def create_evaluation(
        self,
        candidate_name: str,
        job_title: str,
        resume_summary: Optional[str] = None,
        job_summary: Optional[str] = None,
        intersection_score: Optional[float] = None,
        intersection_notes: Optional[str] = None,
        pro_arguments: Optional[List[Dict]] = None,
        anti_arguments: Optional[List[Dict]] = None,
        final_decision: Optional[str] = None,
        decision_confidence: Optional[float] = None,
        decision_reasoning: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new hiring evaluation record

        Args:
            candidate_name: Name of the candidate
            job_title: Title of the job position
            resume_summary: Summary of the resume analysis
            job_summary: Summary of the job requirements analysis
            intersection_score: Compatibility score (0.0 to 1.0)
            intersection_notes: Notes about the intersection analysis
            pro_arguments: List of pro-hire arguments
            anti_arguments: List of anti-hire arguments
            final_decision: Final decision ('HIRE' or 'REJECT')
            decision_confidence: Confidence in the decision (0.0 to 1.0)
            decision_reasoning: Reasoning for the final decision

        Returns:
            Dictionary containing the created record
        """
        data = {
            "candidate_name": candidate_name,
            "job_title": job_title,
            "resume_summary": resume_summary,
            "job_summary": job_summary,
            "intersection_score": intersection_score,
            "intersection_notes": intersection_notes,
            "pro_arguments": json.dumps(pro_arguments) if pro_arguments else None,
            "anti_arguments": json.dumps(anti_arguments) if anti_arguments else None,
            "final_decision": final_decision.upper() if final_decision else None,
            "decision_confidence": decision_confidence,
            "decision_reasoning": decision_reasoning,
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        response = self.client.table("hiring_evaluations").insert(data).execute()

        if response.data:
            return response.data[0]
        else:
            raise Exception("Failed to create evaluation record")

    async def get_evaluation(self, evaluation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a hiring evaluation by ID

        Args:
            evaluation_id: UUID of the evaluation

        Returns:
            Dictionary containing the evaluation record or None if not found
        """
        response = (
            self.client.table("hiring_evaluations")
            .select("*")
            .eq("id", evaluation_id)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    async def get_evaluations_by_candidate(
        self, candidate_name: str
    ) -> List[Dict[str, Any]]:
        """
        Get all evaluations for a specific candidate

        Args:
            candidate_name: Name of the candidate

        Returns:
            List of evaluation records
        """
        response = (
            self.client.table("hiring_evaluations")
            .select("*")
            .eq("candidate_name", candidate_name)
            .execute()
        )
        return response.data or []

    async def get_evaluations_by_job(self, job_title: str) -> List[Dict[str, Any]]:
        """
        Get all evaluations for a specific job title

        Args:
            job_title: Title of the job position

        Returns:
            List of evaluation records
        """
        response = (
            self.client.table("hiring_evaluations")
            .select("*")
            .eq("job_title", job_title)
            .execute()
        )
        return response.data or []

    async def get_evaluations_by_decision(self, decision: str) -> List[Dict[str, Any]]:
        """
        Get all evaluations with a specific decision

        Args:
            decision: Decision to filter by ('HIRE' or 'REJECT')

        Returns:
            List of evaluation records
        """
        response = (
            self.client.table("hiring_evaluations")
            .select("*")
            .eq("final_decision", decision.upper())
            .execute()
        )
        return response.data or []

    async def get_recent_evaluations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent evaluations

        Args:
            limit: Maximum number of records to return

        Returns:
            List of recent evaluation records
        """
        response = (
            self.client.table("hiring_evaluations")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

    async def update_evaluation(
        self, evaluation_id: str, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing evaluation record

        Args:
            evaluation_id: UUID of the evaluation to update
            **kwargs: Fields to update

        Returns:
            Updated evaluation record or None if not found
        """
        # Convert decision to uppercase if provided
        if "final_decision" in kwargs:
            kwargs["final_decision"] = kwargs["final_decision"].upper()

        # Convert arguments to JSON if provided
        if "pro_arguments" in kwargs and kwargs["pro_arguments"]:
            kwargs["pro_arguments"] = json.dumps(kwargs["pro_arguments"])

        if "anti_arguments" in kwargs and kwargs["anti_arguments"]:
            kwargs["anti_arguments"] = json.dumps(kwargs["anti_arguments"])

        response = (
            self.client.table("hiring_evaluations")
            .update(kwargs)
            .eq("id", evaluation_id)
            .execute()
        )

        if response.data:
            return response.data[0]
        return None

    async def delete_evaluation(self, evaluation_id: str) -> bool:
        """
        Delete an evaluation record

        Args:
            evaluation_id: UUID of the evaluation to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        response = (
            self.client.table("hiring_evaluations")
            .delete()
            .eq("id", evaluation_id)
            .execute()
        )
        return len(response.data) > 0

    async def get_evaluation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about hiring evaluations

        Returns:
            Dictionary containing various statistics
        """
        # Get total count
        total_response = (
            self.client.table("hiring_evaluations")
            .select("id", count="exact")
            .execute()
        )
        total_count = total_response.count or 0

        # Get hire count
        hire_response = (
            self.client.table("hiring_evaluations")
            .select("id", count="exact")
            .eq("final_decision", "HIRE")
            .execute()
        )
        hire_count = hire_response.count or 0

        # Get reject count
        reject_response = (
            self.client.table("hiring_evaluations")
            .select("id", count="exact")
            .eq("final_decision", "REJECT")
            .execute()
        )
        reject_count = reject_response.count or 0

        # Calculate hire rate
        hire_rate = (hire_count / total_count * 100) if total_count > 0 else 0

        return {
            "total_evaluations": total_count,
            "hire_count": hire_count,
            "reject_count": reject_count,
            "hire_rate_percentage": round(hire_rate, 2),
            "average_intersection_score": None,  # Would need a more complex query
            "average_decision_confidence": None,  # Would need a more complex query
        }


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_client():
        # Initialize client (you'll need to set environment variables)
        client = HiringEvaluationsClient()

        # Create a test evaluation
        evaluation = await client.create_evaluation(
            candidate_name="John Doe",
            job_title="Software Engineer",
            resume_summary="Experienced developer with Python and JavaScript skills",
            job_summary="Mid-level position requiring Python and React",
            intersection_score=0.85,
            intersection_notes="Strong technical skills match",
            pro_arguments=[
                {"argument": "Strong technical background", "confidence": 0.9}
            ],
            anti_arguments=[
                {"argument": "Limited leadership experience", "confidence": 0.6}
            ],
            final_decision="HIRE",
            decision_confidence=0.8,
            decision_reasoning="Candidate's technical skills outweigh concerns",
        )

        print(f"Created evaluation: {evaluation['id']}")

        # Get statistics
        stats = await client.get_evaluation_stats()
        print(f"Statistics: {stats}")

    # Uncomment to test
    # asyncio.run(test_client())
