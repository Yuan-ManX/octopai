"""
Evolution Engine
Core engine for the self-evolution system
"""

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
from .config import EvolutionConfig


@dataclass
class EvolutionResult:
    """Result of an evolution run"""
    frontier: List[Tuple[str, float]]
    best_program: str
    best_score: float
    iterations_completed: int
    total_cost_usd: float = 0.0
    timestamp: str = ""


@dataclass
class IterationEvent:
    """Event emitted during evolution iterations"""
    event_type: str
    iteration: Optional[int] = None
    data: Dict[str, Any] = None


class EvolutionEngine:
    """
    Self-evolving agent engine
    
    This engine implements a five-stage evolution cycle:
    1. Base Agent - Attempts tasks using current best configuration
    2. Proposer - Analyzes failures and suggests improvements
    3. Generator - Creates proposed changes (skills or prompts)
    4. Evaluator - Measures performance of new variants
    5. Frontier - Tracks top-performing configurations
    """
    
    def __init__(self, config: Optional[EvolutionConfig] = None):
        """
        Initialize the evolution engine
        
        Args:
            config: Evolution configuration, uses defaults if not provided
        """
        self.config = config or EvolutionConfig()
        self._event_callbacks: List[Callable[[IterationEvent], None]] = []
        self._iteration_count = 0
        self._total_cost = 0.0
        self._frontier: List[Tuple[str, float]] = []
        
        # Paths for state management
        self._state_dir = Path(".octopai") / "evolution"
        self._state_dir.mkdir(parents=True, exist_ok=True)
        
        self._feedback_path = self._state_dir / "feedback_history.md"
        self._checkpoint_path = self._state_dir / "checkpoint.json"
    
    def on_event(self, callback: Callable[[IterationEvent], None]) -> None:
        """
        Register an event callback
        
        Args:
            callback: Function to call when events occur
        """
        self._event_callbacks.append(callback)
    
    def _emit(self, event_type: str, iteration: Optional[int] = None, **data: Any) -> None:
        """
        Emit an event to all registered callbacks
        
        Args:
            event_type: Type of event
            iteration: Current iteration number
            **data: Additional event data
        """
        event = IterationEvent(event_type=event_type, iteration=iteration, data=data)
        for callback in self._event_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")
    
    def _save_checkpoint(self, iteration: int) -> None:
        """
        Save current state for resume
        
        Args:
            iteration: Current iteration number
        """
        checkpoint = {
            "iteration": iteration,
            "frontier": self._frontier,
            "total_cost": self._total_cost,
            "timestamp": datetime.now().isoformat()
        }
        self._checkpoint_path.write_text(json.dumps(checkpoint, indent=2))
    
    def _load_checkpoint(self) -> Optional[Dict[str, Any]]:
        """
        Load checkpoint if exists
        
        Returns:
            Checkpoint data or None if no checkpoint
        """
        if not self._checkpoint_path.exists():
            return None
        try:
            return json.loads(self._checkpoint_path.read_text())
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid checkpoint: {e}")
            return None
    
    async def run(self, task_data: Optional[List[Dict]] = None) -> EvolutionResult:
        """
        Run the evolution loop
        
        Args:
            task_data: Optional list of task data for evaluation
            
        Returns:
            EvolutionResult with final state
        """
        self._emit("loop_start", data={"config": self.config.__dict__})
        
        # Handle continue mode
        if self.config.continue_mode:
            checkpoint = self._load_checkpoint()
            if checkpoint:
                self._iteration_count = checkpoint.get("iteration", 0)
                self._frontier = checkpoint.get("frontier", [])
                self._total_cost = checkpoint.get("total_cost", 0.0)
                self._emit("resume", data={"checkpoint": checkpoint})
        
        # Initialize frontier with baseline if empty
        if not self._frontier:
            baseline_score = await self._evaluate_baseline(task_data)
            self._frontier = [("baseline", baseline_score)]
            self._emit("baseline", data={"score": baseline_score})
        
        no_improvement_count = 0
        
        # Main evolution loop
        for i in range(self._iteration_count, self.config.max_iterations):
            current_iteration = i + 1
            self._emit("iter_start", iteration=current_iteration, data={"total": self.config.max_iterations})
            
            # Select parent from frontier
            parent = self._select_parent(current_iteration)
            
            # Simulate running the agent and collecting failures
            failures = await self._collect_failures(parent, task_data)
            
            if not failures:
                self._emit("iter_skip", iteration=current_iteration, data={"reason": "no_failures"})
                continue
            
            # Generate mutation based on failures
            mutation_result = await self._generate_mutation(parent, failures, current_iteration)
            
            if not mutation_result:
                no_improvement_count += 1
                self._emit("iter_skip", iteration=current_iteration, data={"reason": "mutation_failed"})
            else:
                child_name, score = mutation_result
                
                # Update frontier
                added = self._update_frontier(child_name, score)
                
                if added:
                    no_improvement_count = 0
                    self._emit("improvement", iteration=current_iteration, data={
                        "program": child_name,
                        "score": score
                    })
                else:
                    no_improvement_count += 1
                    self._emit("discarded", iteration=current_iteration, data={
                        "program": child_name,
                        "score": score
                    })
            
            # Save checkpoint
            self._save_checkpoint(current_iteration)
            
            # Check early stopping
            if no_improvement_count >= self.config.no_improvement_limit:
                self._emit("early_stop", iteration=current_iteration, data={
                    "reason": f"no_improvement_for_{self.config.no_improvement_limit}_iters"
                })
                break
            
            self._iteration_count = current_iteration
        
        # Prepare final result
        best_program, best_score = self._frontier[0] if self._frontier else ("baseline", 0.0)
        
        result = EvolutionResult(
            frontier=self._frontier,
            best_program=best_program,
            best_score=best_score,
            iterations_completed=self._iteration_count,
            total_cost_usd=self._total_cost,
            timestamp=datetime.now().isoformat()
        )
        
        self._emit("loop_complete", data={"result": result.__dict__})
        
        return result
    
    async def _evaluate_baseline(self, task_data: Optional[List[Dict]] = None) -> float:
        """
        Evaluate baseline performance
        
        Args:
            task_data: Task data for evaluation
            
        Returns:
            Baseline score (0.0 - 1.0)
        """
        # Simulated evaluation - in real implementation this runs the agent
        await asyncio.sleep(0.5)
        return 0.42  # Initial baseline score
    
    def _select_parent(self, iteration: int) -> str:
        """
        Select parent program from frontier
        
        Args:
            iteration: Current iteration number
            
        Returns:
            Selected parent program name
        """
        if self.config.selection_strategy == "best":
            return self._frontier[0][0] if self._frontier else "baseline"
        elif self.config.selection_strategy == "random":
            import random
            return random.choice(self._frontier)[0] if self._frontier else "baseline"
        else:  # round_robin
            idx = (iteration - 1) % len(self._frontier) if self._frontier else 0
            return self._frontier[idx][0] if self._frontier else "baseline"
    
    async def _collect_failures(self, parent: str, task_data: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Collect failure cases from parent program
        
        Args:
            parent: Parent program name
            task_data: Task data
            
        Returns:
            List of failure cases
        """
        # Simulated failure collection
        await asyncio.sleep(0.3)
        
        # Return some sample failures for demonstration
        return [
            {
                "task": "Sample Task 1",
                "error": "Incorrect reasoning pattern",
                "category": "reasoning"
            },
            {
                "task": "Sample Task 2",
                "error": "Missing tool usage",
                "category": "tools"
            }
        ]
    
    async def _generate_mutation(self, parent: str, failures: List[Dict], iteration: int) -> Optional[Tuple[str, float]]:
        """
        Generate and evaluate a mutation
        
        Args:
            parent: Parent program name
            failures: List of failure cases
            iteration: Current iteration
            
        Returns:
            Tuple of (child_name, score) or None if failed
        """
        # Simulated mutation generation
        await asyncio.sleep(0.8)
        
        child_name = f"iter-{self.config.evolution_mode}-{iteration}"
        
        # Simulated evaluation - random improvement
        import random
        parent_score = next((s for n, s in self._frontier if n == parent), 0.42)
        score = parent_score + (random.random() - 0.3) * 0.2
        score = max(0.0, min(1.0, score))
        
        # Add some cost
        self._total_cost += random.uniform(0.01, 0.05)
        
        return (child_name, score)
    
    def _update_frontier(self, program_name: str, score: float) -> bool:
        """
        Update the frontier with a new program
        
        Args:
            program_name: Name of program to add
            score: Score of the program
            
        Returns:
            True if program was added to frontier
        """
        # Add new entry
        self._frontier.append((program_name, score))
        
        # Sort by score descending
        self._frontier.sort(key=lambda x: x[1], reverse=True)
        
        # Trim to frontier size
        if len(self._frontier) > self.config.frontier_size:
            removed = self._frontier.pop()
            return removed[0] != program_name
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current evolution status
        
        Returns:
            Status dictionary
        """
        return {
            "iteration": self._iteration_count,
            "max_iterations": self.config.max_iterations,
            "frontier": self._frontier,
            "total_cost": self._total_cost,
            "config": self.config.__dict__
        }
    
    def reset(self) -> None:
        """Reset the evolution engine state"""
        self._iteration_count = 0
        self._total_cost = 0.0
        self._frontier = []
        
        if self._checkpoint_path.exists():
            self._checkpoint_path.unlink()
        
        if self._feedback_path.exists():
            self._feedback_path.unlink()
        
        self._emit("reset")
