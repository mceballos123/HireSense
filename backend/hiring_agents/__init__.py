"""
uAgents Hiring System Package
=============================

This package contains all the uAgents for the hiring system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from models directory
from models.models import *

# Import from helper-func directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'helper-func'))
from llm_client import SimpleLLMAgent

# Import agents
from .job_parser_agent import JobParserAgent
from .resume_parser_agent import ResumeParserAgent
from .intersection_agent import IntersectionAgent
from .pro_hire_agent import ProHireAgent
from .anti_hire_agent import AntiHireAgent
from .decision_agent import DecisionAgent
from .coordinator_agent import HiringCoordinator

__all__ = [
    "SimpleLLMAgent",
    "JobParserAgent",
    "ResumeParserAgent",
    "IntersectionAgent",
    "ProHireAgent",
    "AntiHireAgent",
    "DecisionAgent",
    "HiringCoordinator",
]
