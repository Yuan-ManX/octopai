"""
Skill Generator Module
Generates new skills from ideas and templates
"""

import random
from typing import List, Dict, Any

from ..models import EvolvableSkill, SkillType


class SkillGenerator:
    """Generates evolved skills from improvement ideas and templates"""

    def __init__(self, template_registry):
        self.template_registry = template_registry

    def generate_from_idea(self, idea: Dict[str, Any], 
                          use_templates: bool = True,
                          exploration_rate: float = 0.3) -> EvolvableSkill:
        """Generate a skill from an improvement idea"""
        
        if use_templates and random.random() < 0.72:
            category = self._infer_category(idea)
            templates = self.template_registry.get_templates_by_category(category)
            
            if templates:
                template = random.choice(templates)
                
                if random.random() < exploration_rate:
                    mutation_types = ['optimization', 'robustness', 'precision', 
                                     'creativity', 'efficiency', 'comprehensive']
                    template = self.template_registry.mutate_template(
                        template, random.choice(mutation_types)
                    )
                
                context = {
                    "objective": idea.get("description", "")[:120],
                    "description": idea["title"],
                    "task_type": idea.get("type", "general"),
                    "variant_type": idea.get("type", "standard")
                }
                
                skill = self.template_registry.generate_skill_from_template(template, context)
                skill.quality_score = random.uniform(6.8, 9.6)
                skill.adaptation_score = random.uniform(5.8, 8.6)
                skill.generalization_score = random.uniform(5.8, 8.6)
                return skill
        
        return self._create_custom_skill(idea)

    def generate_batch(self, ideas: List[Dict[str, Any]], 
                      max_skills: int = 3,
                      exploration_rate: float = 0.3) -> List[EvolvableSkill]:
        """Generate a batch of skills from multiple ideas"""
        skills = []
        
        for idea in ideas[:max_skills]:
            skill = self.generate_from_idea(idea, use_templates=True, 
                                          exploration_rate=exploration_rate)
            skills.append(skill)
        
        return skills

    def _create_custom_skill(self, idea: Dict) -> EvolvableSkill:
        import uuid
        from datetime import datetime
        return EvolvableSkill(
            skill_id=str(uuid.uuid4()),
            name=idea["title"],
            skill_type=self._infer_category(idea),
            description=idea["description"],
            version="1.0.0",
            success_rate=random.uniform(0.68, 0.92),
            quality_score=random.uniform(6.6, 9.4),
            adaptation_score=random.uniform(5.6, 8.4),
            generalization_score=random.uniform(5.6, 8.4),
            tags=["auto-generated", "custom", idea.get("type", "new"), "iteration-derived"],
            created_at=datetime.now()
        )

    def _infer_category(self, idea: Dict) -> SkillType:
        title_lower = idea.get("title", "").lower()
        desc_lower = idea.get("description", "").lower()
        combined = f"{title_lower} {desc_lower}"

        category_keywords = {
            SkillType.CODE_GENERATION: ["code", "program", "develop", "software", "architect", "debug"],
            SkillType.DATA_ANALYSIS: ["data", "analy", "visual", "pattern", "mining", "insight"],
            SkillType.RESEARCH: ["research", "literature", "hypothesis", "study", "investigate", "analyze"],
            SkillType.COMMUNICATION: ["communicat", "write", "report", "content", "document", "express"],
            SkillType.TOOL_USE: ["tool", "api", "integrat", "interface", "connect"],
            SkillType.TASK_EXECUTION: ["task", "execut", "automat", "process", "workflow"]
        }

        best_match = SkillType.TASK_EXECUTION
        best_score = 0

        for skill_type, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in combined)
            if score > best_score:
                best_score = score
                best_match = skill_type

        return best_match
