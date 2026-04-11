"""
SkillBank - Octopai's Hierarchical Skill Library System

This module provides Octopai's proprietary hierarchical skill library that
organizes knowledge into general skills for universal strategic guidance
and task-specific skills for category-level heuristics. Features include
dynamic skill evolution and efficient retrieval mechanisms.
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path


class SkillType(Enum):
    """Types of skills in the SkillBank"""
    GENERAL = "general"
    TASK_SPECIFIC = "task_specific"
    COMMON_MISTAKE = "common_mistake"


@dataclass
class SkillPrinciple:
    """A principle or heuristic within a skill"""
    principle_id: str
    description: str
    when_to_apply: Optional[str] = None
    example_usage: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "principle_id": self.principle_id,
            "description": self.description,
            "when_to_apply": self.when_to_apply,
            "example_usage": self.example_usage
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillPrinciple':
        return cls(**data)


@dataclass
class BankedSkill:
    """A skill stored in the SkillBank with enhanced structure"""
    skill_id: str
    title: str
    skill_type: SkillType
    principles: List[SkillPrinciple] = field(default_factory=list)
    when_to_apply: str = ""
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def effectiveness_score(self) -> float:
        """Calculate effectiveness score based on usage"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5
        return self.success_count / total
    
    def record_success(self):
        """Record a successful application of this skill"""
        self.success_count += 1
        self.updated_at = datetime.now().isoformat()
    
    def record_failure(self):
        """Record a failed application of this skill"""
        self.failure_count += 1
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "title": self.title,
            "skill_type": self.skill_type.value,
            "principles": [p.to_dict() for p in self.principles],
            "when_to_apply": self.when_to_apply,
            "category": self.category,
            "tags": self.tags,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BankedSkill':
        data = data.copy()
        data['skill_type'] = SkillType(data['skill_type'])
        data['principles'] = [SkillPrinciple.from_dict(p) for p in data.get('principles', [])]
        return cls(**data)


@dataclass
class CommonMistake:
    """A common mistake with analysis and avoidance guidance"""
    mistake_id: str
    description: str
    why_it_happens: str = ""
    how_to_avoid: str = ""
    category: Optional[str] = None
    occurrence_count: int = 0
    last_occurred: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def record_occurrence(self):
        """Record an occurrence of this mistake"""
        self.occurrence_count += 1
        self.last_occurred = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mistake_id": self.mistake_id,
            "description": self.description,
            "why_it_happens": self.why_it_happens,
            "how_to_avoid": self.how_to_avoid,
            "category": self.category,
            "occurrence_count": self.occurrence_count,
            "last_occurred": self.last_occurred,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommonMistake':
        return cls(**data)


class SkillBank:
    """
    Hierarchical Skill Library System
    
    Features:
    - General skills for universal strategic guidance
    - Task-specific skills for category-level heuristics
    - Common mistakes with avoidance guidance
    - Dynamic skill evolution during usage
    - Efficient retrieval mechanisms
    - Usage tracking and effectiveness metrics
    """
    
    def __init__(self, storage_dir: str = "./SkillBank"):
        self.storage_dir = Path(storage_dir)
        self.skills_file = self.storage_dir / "skill_bank.json"
        
        self.general_skills: Dict[str, BankedSkill] = {}
        self.task_specific_skills: Dict[str, List[BankedSkill]] = {}
        self.common_mistakes: Dict[str, CommonMistake] = {}
        
        self._initialize_storage()
        self._load_skill_bank()
    
    def _initialize_storage(self):
        """Initialize storage directory"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.skills_file.exists():
            self._save_skill_bank()
    
    def _load_skill_bank(self):
        """Load skill bank from disk"""
        if self.skills_file.exists():
            try:
                with open(self.skills_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for skill_data in data.get('general_skills', []):
                    skill = BankedSkill.from_dict(skill_data)
                    self.general_skills[skill.skill_id] = skill
                
                for category, skills_data in data.get('task_specific_skills', {}).items():
                    self.task_specific_skills[category] = [
                        BankedSkill.from_dict(sd) for sd in skills_data
                    ]
                
                for mistake_data in data.get('common_mistakes', []):
                    mistake = CommonMistake.from_dict(mistake_data)
                    self.common_mistakes[mistake.mistake_id] = mistake
                    
            except Exception as e:
                print(f"Error loading skill bank: {e}")
    
    def _save_skill_bank(self):
        """Save skill bank to disk"""
        data = {
            'general_skills': [s.to_dict() for s in self.general_skills.values()],
            'task_specific_skills': {
                cat: [s.to_dict() for s in skills]
                for cat, skills in self.task_specific_skills.items()
            },
            'common_mistakes': [m.to_dict() for m in self.common_mistakes.values()]
        }
        
        with open(self.skills_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _generate_skill_id(self, title: str, skill_type: SkillType) -> str:
        """Generate a unique skill ID"""
        prefix = "gen" if skill_type == SkillType.GENERAL else "tsk"
        base = f"{prefix}_{title.lower().replace(' ', '_')}"
        base_hash = hashlib.md5(base.encode()).hexdigest()[:8]
        return f"{base}_{base_hash}"
    
    def _generate_mistake_id(self, description: str) -> str:
        """Generate a unique mistake ID"""
        base = f"err_{description.lower().replace(' ', '_')}"
        base_hash = hashlib.md5(base.encode()).hexdigest()[:8]
        return f"{base}_{base_hash}"
    
    def add_general_skill(
        self,
        title: str,
        principles: List[Dict[str, str]],
        when_to_apply: str = "",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BankedSkill:
        """
        Add a general skill for universal strategic guidance
        
        Args:
            title: Skill title
            principles: List of principle dicts with description and when_to_apply
            when_to_apply: When this skill should be applied
            tags: Optional tags
            metadata: Optional metadata
            
        Returns:
            Created BankedSkill
        """
        skill_id = self._generate_skill_id(title, SkillType.GENERAL)
        
        principle_objects = []
        for i, p in enumerate(principles):
            principle_objects.append(SkillPrinciple(
                principle_id=f"{skill_id}_p{i}",
                description=p.get('description', ''),
                when_to_apply=p.get('when_to_apply'),
                example_usage=p.get('example_usage')
            ))
        
        skill = BankedSkill(
            skill_id=skill_id,
            title=title,
            skill_type=SkillType.GENERAL,
            principles=principle_objects,
            when_to_apply=when_to_apply,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.general_skills[skill_id] = skill
        self._save_skill_bank()
        return skill
    
    def add_task_specific_skill(
        self,
        category: str,
        title: str,
        principles: List[Dict[str, str]],
        when_to_apply: str = "",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BankedSkill:
        """
        Add a task-specific skill for category-level heuristics
        
        Args:
            category: Task category
            title: Skill title
            principles: List of principle dicts
            when_to_apply: When this skill should be applied
            tags: Optional tags
            metadata: Optional metadata
            
        Returns:
            Created BankedSkill
        """
        skill_id = self._generate_skill_id(title, SkillType.TASK_SPECIFIC)
        
        principle_objects = []
        for i, p in enumerate(principles):
            principle_objects.append(SkillPrinciple(
                principle_id=f"{skill_id}_p{i}",
                description=p.get('description', ''),
                when_to_apply=p.get('when_to_apply'),
                example_usage=p.get('example_usage')
            ))
        
        skill = BankedSkill(
            skill_id=skill_id,
            title=title,
            skill_type=SkillType.TASK_SPECIFIC,
            principles=principle_objects,
            when_to_apply=when_to_apply,
            category=category,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        if category not in self.task_specific_skills:
            self.task_specific_skills[category] = []
        self.task_specific_skills[category].append(skill)
        self._save_skill_bank()
        return skill
    
    def add_common_mistake(
        self,
        description: str,
        why_it_happens: str = "",
        how_to_avoid: str = "",
        category: Optional[str] = None
    ) -> CommonMistake:
        """
        Add a common mistake with avoidance guidance
        
        Args:
            description: Description of the mistake
            why_it_happens: Why this mistake happens
            how_to_avoid: How to avoid this mistake
            category: Optional category
            
        Returns:
            Created CommonMistake
        """
        mistake_id = self._generate_mistake_id(description)
        
        mistake = CommonMistake(
            mistake_id=mistake_id,
            description=description,
            why_it_happens=why_it_happens,
            how_to_avoid=how_to_avoid,
            category=category
        )
        
        self.common_mistakes[mistake_id] = mistake
        self._save_skill_bank()
        return mistake
    
    def get_general_skills(
        self,
        top_k: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> List[BankedSkill]:
        """
        Get general skills, optionally filtered and ranked
        
        Args:
            top_k: Maximum number of skills to return
            tags: Optional tag filter
            
        Returns:
            List of BankedSkill objects
        """
        skills = list(self.general_skills.values())
        
        if tags:
            skills = [s for s in skills if any(t in s.tags for t in tags)]
        
        skills.sort(key=lambda x: x.effectiveness_score, reverse=True)
        
        if top_k:
            skills = skills[:top_k]
        
        return skills
    
    def get_task_specific_skills(
        self,
        category: str,
        top_k: Optional[int] = None
    ) -> List[BankedSkill]:
        """
        Get task-specific skills for a category
        
        Args:
            category: Task category
            top_k: Maximum number of skills to return
            
        Returns:
            List of BankedSkill objects
        """
        skills = self.task_specific_skills.get(category, [])
        skills.sort(key=lambda x: x.effectiveness_score, reverse=True)
        
        if top_k:
            skills = skills[:top_k]
        
        return skills
    
    def get_common_mistakes(
        self,
        category: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[CommonMistake]:
        """
        Get common mistakes, optionally filtered
        
        Args:
            category: Optional category filter
            top_k: Maximum number of mistakes to return
            
        Returns:
            List of CommonMistake objects
        """
        mistakes = list(self.common_mistakes.values())
        
        if category:
            mistakes = [m for m in mistakes if m.category == category]
        
        mistakes.sort(key=lambda x: x.occurrence_count, reverse=True)
        
        if top_k:
            mistakes = mistakes[:top_k]
        
        return mistakes
    
    def record_skill_success(self, skill_id: str) -> bool:
        """Record a successful skill application"""
        if skill_id in self.general_skills:
            self.general_skills[skill_id].record_success()
            self._save_skill_bank()
            return True
        
        for category, skills in self.task_specific_skills.items():
            for skill in skills:
                if skill.skill_id == skill_id:
                    skill.record_success()
                    self._save_skill_bank()
                    return True
        
        return False
    
    def record_skill_failure(self, skill_id: str) -> bool:
        """Record a failed skill application"""
        if skill_id in self.general_skills:
            self.general_skills[skill_id].record_failure()
            self._save_skill_bank()
            return True
        
        for category, skills in self.task_specific_skills.items():
            for skill in skills:
                if skill.skill_id == skill_id:
                    skill.record_failure()
                    self._save_skill_bank()
                    return True
        
        return False
    
    def record_mistake_occurrence(self, mistake_id: str) -> bool:
        """Record an occurrence of a mistake"""
        if mistake_id in self.common_mistakes:
            self.common_mistakes[mistake_id].record_occurrence()
            self._save_skill_bank()
            return True
        return False
    
    def get_skill_injection_context(
        self,
        category: Optional[str] = None,
        general_top_k: int = 6,
        task_specific_top_k: int = 5,
        mistake_top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Get a complete skill injection context for agent prompting
        
        Args:
            category: Optional task category
            general_top_k: Number of general skills to include
            task_specific_top_k: Number of task-specific skills to include
            mistake_top_k: Number of common mistakes to include
            
        Returns:
            Dictionary with skills and mistakes formatted for injection
        """
        context = {
            'general_skills': [],
            'task_specific_skills': [],
            'common_mistakes': []
        }
        
        general_skills = self.get_general_skills(top_k=general_top_k)
        for skill in general_skills:
            context['general_skills'].append({
                'title': skill.title,
                'principles': [p.description for p in skill.principles],
                'when_to_apply': skill.when_to_apply,
                'effectiveness': skill.effectiveness_score
            })
        
        if category:
            task_skills = self.get_task_specific_skills(category, top_k=task_specific_top_k)
            for skill in task_skills:
                context['task_specific_skills'].append({
                    'title': skill.title,
                    'principles': [p.description for p in skill.principles],
                    'when_to_apply': skill.when_to_apply,
                    'effectiveness': skill.effectiveness_score
                })
        
        mistakes = self.get_common_mistakes(category=category, top_k=mistake_top_k)
        for mistake in mistakes:
            context['common_mistakes'].append({
                'description': mistake.description,
                'why_it_happens': mistake.why_it_happens,
                'how_to_avoid': mistake.how_to_avoid
            })
        
        return context
    
    def format_for_prompt_injection(self, context: Dict[str, Any]) -> str:
        """
        Format skill context for injection into agent prompts
        
        Args:
            context: Skill context from get_skill_injection_context
            
        Returns:
            Formatted string ready for prompt injection
        """
        parts = []
        
        parts.append("## Strategic Guidance\n")
        
        if context['general_skills']:
            parts.append("### General Principles\n")
            for skill in context['general_skills']:
                parts.append(f"**{skill['title']}**")
                parts.append(f"When to apply: {skill['when_to_apply']}")
                for principle in skill['principles']:
                    parts.append(f"- {principle}")
                parts.append("")
        
        if context['task_specific_skills']:
            parts.append("### Task-Specific Heuristics\n")
            for skill in context['task_specific_skills']:
                parts.append(f"**{skill['title']}**")
                parts.append(f"When to apply: {skill['when_to_apply']}")
                for principle in skill['principles']:
                    parts.append(f"- {principle}")
                parts.append("")
        
        if context['common_mistakes']:
            parts.append("### Common Pitfalls to Avoid\n")
            for mistake in context['common_mistakes']:
                parts.append(f"⚠️ {mistake['description']}")
                if mistake['why_it_happens']:
                    parts.append(f"Why: {mistake['why_it_happens']}")
                if mistake['how_to_avoid']:
                    parts.append(f"Avoid: {mistake['how_to_avoid']}")
                parts.append("")
        
        return "\n".join(parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get SkillBank statistics"""
        total_general = len(self.general_skills)
        total_task_specific = sum(len(skills) for skills in self.task_specific_skills.values())
        total_mistakes = len(self.common_mistakes)
        total_categories = len(self.task_specific_skills)
        
        general_success_rate = sum(
            s.effectiveness_score for s in self.general_skills.values()
        ) / total_general if total_general > 0 else 0
        
        return {
            'total_general_skills': total_general,
            'total_task_specific_skills': total_task_specific,
            'total_common_mistakes': total_mistakes,
            'total_categories': total_categories,
            'general_skills_success_rate': general_success_rate,
            'categories': list(self.task_specific_skills.keys())
        }
