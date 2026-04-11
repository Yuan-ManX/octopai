"""
Feedback Descent Optimization Algorithm
Adaptive learning with momentum and convergence detection
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models import EvolutionConfig, FeedbackSignal, FeedbackType


class FeedbackDescentOptimizer:
    """Core feedback descent optimization algorithm with adaptive learning"""

    def __init__(self, config: EvolutionConfig = None):
        self.config = config or EvolutionConfig()
        self.velocity: Dict[str, float] = {}
        self.gradient_history: List[float] = []
        self.best_score_ever: float = 0.0
        self.iteration_count: int = 0
        self.patience_counter: int = 0
        self.converged: bool = False

    def compute_gradient(self, current_state: Dict[str, float],
                        target_state: Dict[str, float],
                        feedback_signals: List[FeedbackSignal]) -> Dict[str, float]:
        """Compute gradient based on state difference and feedback"""
        gradients = {}
        
        for key in target_state.keys():
            current_val = current_state.get(key, 0.0)
            target_val = target_state[key]
            
            base_delta = (target_val - current_val) * self.config.learning_rate
            
            signal_influence = 0.0
            for signal in feedback_signals:
                if signal.metric_name == key or key in signal.context:
                    normalized_signal = self._normalize_signal(signal)
                    influence_weight = self._get_feedback_magnitude(signal.feedback_type)
                    signal_influence += normalized_signal * influence_weight
            
            gradient = base_delta + signal_influence * 0.3
            
            gradients[key] = round(gradient, 6)
        
        return gradients

    def apply_momentum_update(self, gradients: Dict[str, float]) -> Dict[str, float]:
        """Apply momentum-based update to smooth optimization trajectory"""
        decay_factor = self.config.decay_factor ** self.iteration_count
        
        updated_gradients = {}
        for metric, grad in gradients.items():
            if metric not in self.velocity:
                self.velocity[metric] = 0.0
            
            momentum_term = self.config.momentum * self.velocity[metric]
            gradient_term = (1 - self.config.momentum) * grad
            
            self.velocity[metric] = momentum_term + gradient_term
            updated_gradients[metric] = round(self.velocity[metric] * decay_factor, 6)
        
        return updated_gradients

    def check_convergence(self, current_score: float) -> bool:
        """Check if optimization has converged using patience mechanism"""
        self.gradient_history.append(current_score)
        
        if current_score > self.best_score_ever:
            self.best_score_ever = current_score
            self.patience_counter = 0
        else:
            self.patience_counter += 1
        
        if self.patience_counter >= self.config.patience:
            self.converged = True
            return True
        
        if len(self.gradient_history) >= self.config.patience:
            recent = self.gradient_history[-self.config.patience:]
            variance = sum((s - sum(recent)/len(recent))**2 for s in recent) / len(recent)
            
            if variance < self.config.convergence_threshold:
                self.converged = True
                return True
        
        self.iteration_count += 1
        return False

    def get_adaptive_learning_rate(self) -> float:
        """Dynamically adjust learning rate based on progress"""
        base_lr = self.config.learning_rate
        
        if self.iteration_count == 0:
            return base_lr
        
        progress_ratio = min(1.0, self.iteration_count / self.config.max_iterations)
        
        adaptive_lr = base_lr * (1.0 - 0.5 * progress_ratio)
        
        if self.patience_counter > 0:
            adaptive_lr *= 0.8 ** self.patience_counter
        
        return max(adaptive_lr, base_lr * 0.01)

    def _normalize_signal(self, signal: FeedbackSignal) -> float:
        min_val, max_val = signal.expected_range
        range_size = max_val - min_val
        if range_size == 0:
            return 0.0
        return 2 * (signal.value - min_val) / range_size - 1

    def _get_feedback_magnitude(self, feedback_type: FeedbackType) -> float:
        magnitudes = {
            FeedbackType.POSITIVE_REINFORCEMENT: 1.0,
            FeedbackType.NEGATIVE_CORRECTION: -1.3,
            FeedbackType.NEUTRAL_OBSERVATION: 0.25,
            FeedbackType.EXPLORATORY_PROBE: 0.6
        }
        return magnitudes.get(feedback_type, 0.5)

    def reset(self):
        self.velocity.clear()
        self.gradient_history.clear()
        self.iteration_count = 0
        self.patience_counter = 0
        self.converged = False
