"""
Shared Models for uAgents Hiring System
======================================

This file contains all the Pydantic models used across the uAgents system.
"""

from typing import List
from pydantic import BaseModel


# Job-related models
class JobParseRequest(BaseModel):
    job_description: str
    job_title: str


class JobParseResponse(BaseModel):
    job_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    key_requirements: List[str]
    analysis: str


# Resume-related models
class ResumeParseRequest(BaseModel):
    resume_content: str
    candidate_name: str


class ResumeParseResponse(BaseModel):
    candidate_name: str
    skills: List[str]
    experience_years: int
    experience_level: str
    key_achievements: List[str]
    analysis: str


# Intersection evaluation models
class IntersectionRequest(BaseModel):
    job_analysis: JobParseResponse
    resume_analysis: ResumeParseResponse


class IntersectionResponse(BaseModel):
    analysis: str
    overall_compatibility: float
    skill_matches: List[str]
    skill_gaps: List[str]
    experience_match: str


# Debate models
class DebateRequest(BaseModel):
    intersection_analysis: IntersectionResponse
    round_number: int
    previous_argument: str = ""


class DebateResponse(BaseModel):
    position: str  # "pro" or "anti"
    argument: str
    confidence: float
    key_points: List[str]


# Decision models
class DecisionRequest(BaseModel):
    pro_arguments: List[DebateResponse]
    anti_arguments: List[DebateResponse]
    intersection_analysis: IntersectionResponse


class DecisionResponse(BaseModel):
    decision: str  # "hire" or "no_hire"
    confidence: float
    reasoning: str
    key_factors: List[str]
