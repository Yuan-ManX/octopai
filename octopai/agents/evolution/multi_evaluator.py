"""
Multi-dimensional Evaluation System
Comprehensive evaluation with multiple scoring dimensions
"""

import random
from typing import Dict, Any, Optional

from ..models import (
    EvolvableSkill, SkillType, EvolutionConfig
)
from .reward_function import RewardFunction


class MultiDimensionalEvaluator:
    """Comprehensive evaluation system with multiple scoring dimensions"""

    def __init__(self, config: EvolutionConfig = None, reward_fn: RewardFunction = None):
        self.config = config or EvolutionConfig()
        self.reward_fn = reward_fn or RewardFunction()

    def evaluate_skill(self, skill: EvolvableSkill,
                      context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}

        dimension_scores = {
            'quality': self._evaluate_quality(skill, context),
            'performance': self._evaluate_performance(skill, context),
            'reliability': self._evaluate_reliability(skill, context),
            'novelty': self._evaluate_novelty(skill, context),
            'adaptation': self._evaluate_adaptation(skill, context),
            'generalization': self._evaluate_generalization(skill, context)
        }

        reward_metrics = {
            'accuracy': dimension_scores['quality'],
            'efficiency': dimension_scores['performance'],
            'style': dimension_scores['reliability'],
            'completeness': dimension_scores['adaptation'],
            'innovation': dimension_scores['novelty']
        }

        reward_result = self.reward_fn.calculate_reward(reward_metrics)

        weighted_total = (
            dimension_scores['quality'] * self.config.quality_weight +
            dimension_scores['performance'] * self.config.performance_weight +
            dimension_scores['reliability'] * self.config.reliability_weight +
            dimension_scores['novelty'] * self.config.novelty_weight
        )

        overall = max(0.0, min(10.0, weighted_total))

        return {
            'dimensions': {k: round(v, 3) for k, v in dimension_scores.items()},
            'reward_analysis': reward_result,
            'weighted_total': round(weighted_total, 3),
            'overall': round(overall, 3),
            'passed': overall >= 6.0,
            'grade': reward_result['grade'],
            'recommendation': self._generate_recommendation(dimension_scores, overall)
        }

    def _evaluate_quality(self, skill: EvolvableSkill, context: Dict) -> float:
        base = skill.quality_score if skill.quality_score > 0 else 7.0
        bonus = 0.0

        if skill.prompt_template:
            prompt_len = len(skill.prompt_template)
            if prompt_len > 150:
                bonus += 0.6
            elif prompt_len > 80:
                bonus += 0.3

            structural_elements = ['step', 'validate', 'constraint', 'output']
            matches = sum(1 for elem in structural_elements if elem in skill.prompt_template.lower())
            bonus += matches * 0.25

        if skill.code_template:
            bonus += 0.4

        return min(10.0, base + bonus + random.uniform(-0.4, 0.7))

    def _evaluate_performance(self, skill: EvolvableSkill, context: Dict) -> float:
        base = 7.0

        if skill.success_rate > 0:
            base = 5.0 + skill.success_rate * 5.0

        if skill.avg_execution_time > 0:
            if skill.avg_execution_time < 1500:
                base += 0.6
            elif skill.avg_execution_time < 3000:
                base += 0.2
            elif skill.avg_execution_time > 6000:
                base -= 0.4

        return max(0.0, min(10.0, base + random.uniform(-0.3, 0.5)))

    def _evaluate_reliability(self, skill: EvolvableSkill, context: Dict) -> float:
        base = 7.5

        if skill.evolution_count > 0:
            stability = max(0.4, 1.0 - skill.evolution_count * 0.04)
            base *= stability

        if skill.tags:
            if 'stable' in skill.tags:
                base += 1.2
            if 'tested' in skill.tags:
                base += 0.8
            if 'production' in skill.tags:
                base += 1.0

        return max(0.0, min(10.0, base + random.uniform(-0.2, 0.4)))

    def _evaluate_novelty(self, skill: EvolvableSkill, context: Dict) -> float:
        base = 5.0

        unique_tags = len(set(skill.tags))
        base += unique_tags * 0.35

        if skill.evolution_count == 0:
            base += 1.2

        if skill.source_template_id:
            if 'variant' in skill.name.lower() or 'optimized' in skill.name.lower():
                base += 0.6
            if 'creative' in skill.tags or 'innovative' in skill.tags:
                base += 1.0

        if skill.parent_skill_id is None:
            base += 0.8

        return max(0.0, min(10.0, base + random.uniform(-0.4, 1.2)))

    def _evaluate_adaptation(self, skill: EvolvableSkill, context: Dict) -> float:
        base = 6.0

        if skill.prompt_template:
            var_count = skill.prompt_template.count('{')
            if var_count > 3:
                base += 1.8
            elif var_count > 1:
                base += 1.0

        if skill.feedback_history:
            recent = skill.feedback_history[-5:]
            avg_adapt = sum(f.get('adaptation_delta', 0) for f in recent) / max(len(recent), 1)
            base += avg_adapt

        adaptable_types = [SkillType.TASK_EXECUTION, SkillType.DATA_ANALYSIS, SkillType.TOOL_USE]
        if skill.skill_type in adaptable_types:
            base += 0.6

        return max(0.0, min(10.0, base + random.uniform(-0.3, 0.7)))

    def _evaluate_generalization(self, skill: EvolvableSkill, context: Dict) -> float:
        base = 6.0

        generalizable_types = [SkillType.TASK_EXECUTION, SkillType.DATA_ANALYSIS, SkillType.RESEARCH]
        if skill.skill_type in generalizable_types:
            base += 1.2

        if skill.evolution_count >= 3:
            base += 0.6

        task_diversity = set()
        for fb in skill.feedback_history[-12:]:
            task_type = fb.get('task_type', 'unknown')
            task_diversity.add(task_type)

        base += len(task_diversity) * 0.18

        if skill.tags and ('universal' in skill.tags or 'versatile' in skill.tags):
            base += 1.0

        return max(0.0, min(10.0, base + random.uniform(-0.4, 0.6)))

    def _generate_recommendation(self, dimensions: Dict[str, float], overall: float) -> str:
        weak_dims = [(name, score) for name, score in dimensions.items() if score < 6.0]
        strong_dims = [(name, score) for name, score in dimensions.items() if score >= 8.0]

        if overall >= 8.5:
            return "Exceptional performance across all dimensions"
        elif overall >= 7.5:
            return "Strong candidate with minor improvements possible"
        elif overall >= 6.0:
            if weak_dims:
                weakest = min(weak_dims, key=lambda x: x[1])
                return f"Focus on improving {weakest[0].replace('_', ' ')}"
            return "Solid performance, ready for integration"
        else:
            weakest = min(dimensions.items(), key=lambda x: x[1])
            return f"Significant improvement needed in {weakest[0].replace('_', ' ')}"
