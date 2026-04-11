"""
Octopai Agents - Skills System Module
Skill templates, generation, and management
"""

from .templates import SkillTemplateRegistry
from .generator import SkillGenerator

__all__ = [
    'SkillTemplateRegistry',
    'SkillGenerator'
]
