"""
Evolution Status and Config Schemas
Schemas for evolution status and configuration
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class EvolutionStatus:
    """Current status of the evolution system"""
    iteration: int = 0
    max_iterations: int = 20
    frontier: List[Tuple[str, float]] = field(default_factory=list)
    total_cost: float = 0.0
    is_running: bool = False
    config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "iteration": self.iteration,
            "max_iterations": self.max_iterations,
            "frontier": [{"name": name, "score": score} for name, score in self.frontier],
            "total_cost": self.total_cost,
            "is_running": self.is_running,
            "config": self.config
        }


@dataclass
class EvolutionConfigRequest:
    """Request to configure evolution"""
    max_iterations: Optional[int] = None
    frontier_size: Optional[int] = None
    no_improvement_limit: Optional[int] = None
    evolution_mode: Optional[str] = None
    selection_strategy: Optional[str] = None
    continue_mode: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, only including non-None values"""
        result = {}
        if self.max_iterations is not None:
            result["max_iterations"] = self.max_iterations
        if self.frontier_size is not None:
            result["frontier_size"] = self.frontier_size
        if self.no_improvement_limit is not None:
            result["no_improvement_limit"] = self.no_improvement_limit
        if self.evolution_mode is not None:
            result["evolution_mode"] = self.evolution_mode
        if self.selection_strategy is not None:
            result["selection_strategy"] = self.selection_strategy
        if self.continue_mode is not None:
            result["continue_mode"] = self.continue_mode
        return result
