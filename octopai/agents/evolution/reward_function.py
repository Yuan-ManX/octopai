"""
Multi-dimensional Reward Calculation Framework
Computes reward scores with weighted dimensions and penalties
"""

from typing import Dict, Any


class RewardFunction:
    """Multi-dimensional reward calculation framework"""

    def __init__(self):
        self.weights = {
            'accuracy': 0.30,
            'efficiency': 0.20,
            'style': 0.15,
            'completeness': 0.20,
            'innovation': 0.15
        }
        self.penalties = {
            'error_severity': -0.5,
            'timeout_penalty': -0.3,
            'repetition_penalty': -0.1
        }

    def calculate_reward(self, metrics: Dict[str, float], 
                        baseline: Dict[str, float] = None) -> Dict[str, Any]:
        """Calculate multi-dimensional reward score"""
        scores = {}
        
        for dimension in self.weights.keys():
            raw_value = metrics.get(dimension, 5.0)
            
            if baseline and dimension in baseline:
                improvement = (raw_value - baseline[dimension]) / max(baseline[dimension], 0.1)
                normalized = min(10.0, max(0.0, 5.0 + improvement * 5))
            else:
                normalized = min(10.0, max(0.0, raw_value))
            
            scores[dimension] = round(normalized, 3)
        
        weighted_total = sum(scores[d] * w for d, w in self.weights.items())
        
        penalty_total = 0.0
        for penalty_name, weight in self.penalties.items():
            if penalty_name in metrics:
                penalty_total += metrics[penalty_name] * abs(weight)
        
        final_score = max(0.0, min(10.0, weighted_total - penalty_total))
        
        return {
            'dimension_scores': scores,
            'weighted_total': round(weighted_total, 3),
            'penalty_total': round(penalty_total, 3),
            'final_score': round(final_score, 3),
            'grade': self._score_to_grade(final_score)
        }

    def _score_to_grade(self, score: float) -> str:
        if score >= 9.5: return 'S+'
        elif score >= 9.0: return 'S'
        elif score >= 8.5: return 'A+'
        elif score >= 8.0: return 'A'
        elif score >= 7.5: return 'B+'
        elif score >= 7.0: return 'B'
        elif score >= 6.5: return 'C+'
        elif score >= 6.0: return 'C'
        else: return 'D'
