"""
AutoResearch Module
Core autonomous research capabilities for Octopai
"""

from .models import (
    ResearchProject, ResearchIdea, Experiment, Paper,
    LiteratureSearch, ResearchStatus, ExperimentStatus, Visibility
)
from .manager import AutoResearchManager

__all__ = [
    "ResearchProject",
    "ResearchIdea", 
    "Experiment",
    "Paper",
    "LiteratureSearch",
    "ResearchStatus",
    "ExperimentStatus",
    "Visibility",
    "AutoResearchManager"
]
