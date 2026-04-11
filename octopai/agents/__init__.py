"""
Octopai Agents Module - Advanced Agent Intelligence System
Self-evolving AI agents with comprehensive skill integration
"""

from .models import (
    AgentInstance, AgentConfig, EvolvableSkill, EvolutionRun,
    TaskExecution, AgentStatus, EvolutionPhase, SkillType,
    EvolutionStrategy, FeedbackType, FeedbackSignal,
    SkillTemplate, EvolutionConfig
)

from .engine import EvolutionEngineManager

__all__ = [
    'AgentInstance', 'AgentConfig', 'EvolvableSkill', 'EvolutionRun',
    'TaskExecution', 'AgentStatus', 'EvolutionPhase', 'SkillType',
    'EvolutionStrategy', 'FeedbackType', 'FeedbackSignal',
    'SkillTemplate', 'EvolutionConfig',
    'EvolutionEngineManager'
]
