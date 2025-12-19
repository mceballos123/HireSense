"""
uAgents Hiring System Package
=============================

This package contains all the uAgents for the hiring system.
Each agent follows the Fetch.ai uAgents best practices with:
- Factory functions for flexible creation
- Versioned protocols
- Proper event lifecycle handlers
- Backward compatibility wrappers
"""

# Import agent classes/factories for convenient access
from .job_parser_agent import JobParserAgent
from .resume_parser_agent import ResumeParserAgent
from .intersection_agent import IntersectionAgent
from .pro_hire_agent import ProHireAgent
from .anti_hire_agent import AntiHireAgent
from .decision_agent import DecisionAgent
from .coordinator_agent import HiringCoordinator

# Export public API
__all__ = [
    "JobParserAgent",
    "ResumeParserAgent",
    "IntersectionAgent",
    "ProHireAgent",
    "AntiHireAgent",
    "DecisionAgent",
    "HiringCoordinator",
]

__version__ = "1.0.0"
