"""
Evolution Engine

This module implements a skill evolution engine using a reflective text evolution approach.
It uses a three-stage pipeline: Executor, Reflector, and Optimizer.
"""

import os
import json
from typing import List, Dict, Any, Optional
from exo.utils.config import Config
from exo.utils.helpers import read_file, write_file
import requests


class EvolutionTrace:
    """
    Represents an execution trace with actionable side information
    """
    
    def __init__(self):
        self.success: bool = False
        self.error_messages: List[str] = []
        self.reasoning_logs: List[str] = []
        self.performance_metrics: Dict[str, Any] = {}
        self.other_info: Dict[str, Any] = {}
    
    def add_error(self, error: str):
        """Add an error message to the trace"""
        self.error_messages.append(error)
    
    def add_reasoning(self, reasoning: str):
        """Add reasoning information to the trace"""
        self.reasoning_logs.append(reasoning)
    
    def add_metric(self, key: str, value: Any):
        """Add a performance metric"""
        self.performance_metrics[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary"""
        return {
            "success": self.success,
            "error_messages": self.error_messages,
            "reasoning_logs": self.reasoning_logs,
            "performance_metrics": self.performance_metrics,
            "other_info": self.other_info
        }


class SkillCandidate:
    """
    Represents a skill candidate in the evolution process
    """
    
    def __init__(self, content: str, version: int = 1):
        self.content = content
        self.version = version
        self.fitness: float = 0.0
        self.trace: Optional[EvolutionTrace] = None
        self.ancestors: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert candidate to dictionary"""
        return {
            "content": self.content,
            "version": self.version,
            "fitness": self.fitness,
            "trace": self.trace.to_dict() if self.trace else None,
            "ancestors": self.ancestors
        }


class EvolutionEngine:
    """
    Evolution Engine for skills
    
    Implements the three-stage pipeline:
    1. Executor: Run candidate and capture traces
    2. Reflector: Analyze traces to diagnose failures
    3. Optimizer: Generate improved candidates
    """
    
    def __init__(self):
        self.config = Config()
        self.pareto_frontier: List[SkillCandidate] = []
        self.max_iterations: int = 10
        self.current_iteration: int = 0
    
    def executor(self, candidate: SkillCandidate) -> EvolutionTrace:
        """
        Stage 1: Execute the candidate and capture complete traces
        
        Args:
            candidate: The skill candidate to execute
            
        Returns:
            EvolutionTrace with actionable side information
        """
        trace = EvolutionTrace()
        
        try:
            # In a real implementation, this would evaluate the skill
            # For now, we'll simulate the execution
            trace.success = True
            trace.add_reasoning("Skill candidate executed successfully")
            trace.add_metric("readability", 0.85)
            trace.add_metric("completeness", 0.75)
            
        except Exception as e:
            trace.success = False
            trace.add_error(str(e))
        
        return trace
    
    def reflector(self, traces: List[EvolutionTrace]) -> str:
        """
        Stage 2: Reflect on traces to diagnose failures and patterns
        
        Uses LLM to analyze collected traces and identify failure modes
        
        Args:
            traces: List of execution traces to analyze
            
        Returns:
            Diagnosis and recommendations for improvement
        """
        # Prepare trace analysis
        trace_analysis = "\n".join([
            f"Trace {i+1}:\n"
            f"  Success: {trace.success}\n"
            f"  Errors: {', '.join(trace.error_messages) if trace.error_messages else 'None'}\n"
            f"  Metrics: {trace.performance_metrics}"
            for i, trace in enumerate(traces)
        ])
        
        # Use OpenRouter API for reflection
        headers = {
            'Authorization': f'Bearer {self.config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "anthropic/claude-4.6-opus",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in analyzing skill evolution traces. "
                               "Identify failure modes, logic breakdowns, and patterns. "
                               "Provide concrete recommendations for improvement."
                },
                {
                    "role": "user",
                    "content": f"Analyze these evolution traces and provide diagnosis and recommendations:\n\n{trace_analysis}"
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', "No diagnosis available")
        except Exception as e:
            return f"Reflection failed: {str(e)}. Using basic improvements."
    
    def optimizer(self, diagnosis: str, current_candidate: SkillCandidate) -> SkillCandidate:
        """
        Stage 3: Generate an improved candidate based on diagnosis
        
        Args:
            diagnosis: The diagnosis from the reflector
            current_candidate: The current skill candidate
            
        Returns:
            Improved skill candidate
        """
        # Use LLM to generate improved candidate
        headers = {
            'Authorization': f'Bearer {self.config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "anthropic/claude-4.6-opus",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in skill improvement. "
                               "Based on the diagnosis, create an improved version of the skill."
                },
                {
                    "role": "user",
                    "content": f"Current skill:\n{current_candidate.content}\n\n"
                               f"Diagnosis:\n{diagnosis}\n\n"
                               f"Please create an improved version of this skill."
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            improved_content = result.get('choices', [{}])[0].get('message', {}).get('content', current_candidate.content)
            
            # Create new candidate
            new_candidate = SkillCandidate(improved_content, version=current_candidate.version + 1)
            new_candidate.ancestors = current_candidate.ancestors + [f"v{current_candidate.version}"]
            
            return new_candidate
            
        except Exception as e:
            print(f"Optimizer failed: {str(e)}. Returning current candidate.")
            return current_candidate
    
    def evaluate_fitness(self, candidate: SkillCandidate) -> float:
        """
        Evaluate the fitness of a candidate
        
        Args:
            candidate: The skill candidate to evaluate
            
        Returns:
            Fitness score between 0 and 1
        """
        if not candidate.trace:
            return 0.0
        
        # Simple fitness calculation based on metrics
        metrics = candidate.trace.performance_metrics
        if not metrics:
            return 0.0
        
        # Average of available metrics
        values = [v for v in metrics.values() if isinstance(v, (int, float))]
        if not values:
            return 0.0
        
        return sum(values) / len(values)
    
    def evolve(self, skill_dir: str, max_iterations: int = 5) -> str:
        """
        Main evolution loop
        
        Args:
            skill_dir: Path to the skill directory
            max_iterations: Maximum number of evolution iterations
            
        Returns:
            Path to the evolved skill directory
        """
        # Read initial skill
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_file):
            raise Exception(f"SKILL.md file not found: {skill_file}")
        
        initial_content = read_file(skill_file)
        current_candidate = SkillCandidate(initial_content)
        
        self.max_iterations = max_iterations
        self.pareto_frontier = [current_candidate]
        
        for iteration in range(max_iterations):
            self.current_iteration = iteration + 1
            print(f"Evolution iteration {self.current_iteration}/{max_iterations}")
            
            # Stage 1: Execute and collect traces
            traces = []
            for candidate in self.pareto_frontier:
                trace = self.executor(candidate)
                candidate.trace = trace
                candidate.fitness = self.evaluate_fitness(candidate)
                traces.append(trace)
            
            # Stage 2: Reflect on traces
            diagnosis = self.reflector(traces)
            print(f"Diagnosis: {diagnosis[:100]}...")
            
            # Stage 3: Generate improved candidates
            new_candidates = []
            for candidate in self.pareto_frontier:
                improved = self.optimizer(diagnosis, candidate)
                new_candidates.append(improved)
            
            # Update Pareto frontier (simplified)
            self.pareto_frontier = sorted(new_candidates, key=lambda x: x.fitness, reverse=True)[:3]
        
        # Select best candidate
        best_candidate = max(self.pareto_frontier, key=lambda x: x.fitness)
        
        # Write evolved skill
        write_file(skill_file, best_candidate.content)
        
        # Save evolution history
        history_file = os.path.join(skill_dir, 'references', 'evolution_history.json')
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        
        history = {
            "initial_version": 1,
            "final_version": best_candidate.version,
            "iterations": max_iterations,
            "best_fitness": best_candidate.fitness,
            "candidates": [c.to_dict() for c in self.pareto_frontier]
        }
        
        write_file(history_file, json.dumps(history, indent=2))
        
        return skill_dir
