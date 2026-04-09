"""
Evolution Configuration
Configuration parameters for the self-evolution system
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EvolutionConfig:
    """Configuration for the evolution engine"""
    
    # Evolution parameters
    max_iterations: int = 20
    frontier_size: int = 3
    no_improvement_limit: int = 5
    concurrency: int = 4
    
    # Evolution mode
    evolution_mode: str = "skill_only"  # skill_only, prompt_only, hybrid
    
    # Data parameters
    train_ratio: float = 0.18
    val_ratio: float = 0.12
    
    # Sampling parameters
    failure_sample_count: int = 3
    categories_per_batch: int = 3
    
    # Cache and state
    cache_enabled: bool = True
    reset_feedback: bool = True
    continue_mode: bool = False
    
    # Selection strategy
    selection_strategy: str = "best"  # best, random, round_robin
    
    # Proposer parameters
    proposer_max_truncation_level: int = 2
    proposer_single_failure_fallback: bool = True
    
    def __post_init__(self):
        """Validate configuration"""
        valid_modes = ["skill_only", "prompt_only", "hybrid"]
        if self.evolution_mode not in valid_modes:
            raise ValueError(f"Invalid evolution_mode: {self.evolution_mode}. Must be one of {valid_modes}")
        
        valid_strategies = ["best", "random", "round_robin"]
        if self.selection_strategy not in valid_strategies:
            raise ValueError(f"Invalid selection_strategy: {self.selection_strategy}. Must be one of {valid_strategies}")
