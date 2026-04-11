"""
Evolution Engine - Octopai's Advanced Skill Evolution System

This module provides Octopai's proprietary skill optimization and evolution system
that continuously improves skills through intelligent reflection, iterative
refinement, and multi-objective optimization. Features include curriculum-based
learning, goal-oriented evolution, self-verification, and meta-cognitive reflection.
"""

import os
import json
import random
from typing import Optional, List, Dict, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import hashlib

from octopai.utils.config import Config
from octopai.utils.helpers import read_file, write_file
from octopai.memory.tracker import InteractionType, InteractionOutcome
import requests


class EvolutionObjective(Enum):
    """Objectives for skill optimization"""
    READABILITY = "readability"
    COMPLETENESS = "completeness"
    EFFICIENCY = "efficiency"
    ROBUSTNESS = "robustness"
    CLARITY = "clarity"
    USABILITY = "usability"
    ADAPTABILITY = "adaptability"
    GENERALIZATION = "generalization"


class GoalPriority(Enum):
    """Priority levels for evolution goals"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class EvolutionGoal:
    """Specific goal for skill evolution"""
    description: str
    priority: GoalPriority = GoalPriority.MEDIUM
    success_criteria: str = ""
    progress_metrics: Dict[str, float] = field(default_factory=dict)
    achieved: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "priority": self.priority.value,
            "success_criteria": self.success_criteria,
            "progress_metrics": self.progress_metrics,
            "achieved": self.achieved,
            "created_at": self.created_at
        }


@dataclass
class CurriculumLevel:
    """A level in the evolution curriculum"""
    level: int
    name: str
    difficulty: float
    task_complexity: float
    required_success_rate: float
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "name": self.name,
            "difficulty": self.difficulty,
            "task_complexity": self.task_complexity,
            "required_success_rate": self.required_success_rate,
            "tasks": self.tasks
        }


@dataclass
class SelfVerificationResult:
    """Result from self-verification process"""
    verification_id: str
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    passed: bool = False
    test_results: Dict[str, bool] = field(default_factory=dict)
    confidence_score: float = 0.0
    issues_found: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "verification_id": self.verification_id,
            "verified_at": self.verified_at,
            "passed": self.passed,
            "test_results": self.test_results,
            "confidence_score": self.confidence_score,
            "issues_found": self.issues_found,
            "recommendations": self.recommendations
        }


@dataclass
class MetaCognitiveReflection:
    """Meta-cognitive reflection on the evolution process itself"""
    reflection_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    process_insights: List[str] = field(default_factory=list)
    strategy_adjustments: List[str] = field(default_factory=list)
    pattern_recognitions: List[str] = field(default_factory=list)
    learning_rate_optimization: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "reflection_id": self.reflection_id,
            "timestamp": self.timestamp,
            "process_insights": self.process_insights,
            "strategy_adjustments": self.strategy_adjustments,
            "pattern_recognitions": self.pattern_recognitions,
            "learning_rate_optimization": self.learning_rate_optimization
        }


@dataclass
class KnowledgeChunk:
    """Atomic unit of knowledge for the knowledge base"""
    chunk_id: str
    content: str
    source: str
    relevance_score: float
    category: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    last_accessed: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "source": self.source,
            "relevance_score": self.relevance_score,
            "category": self.category,
            "created_at": self.created_at,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed
        }


@dataclass
class ActionableSideInfo:
    """Actionable Side Information (ASI) - diagnostic feedback for evolution"""
    error_messages: List[str] = field(default_factory=list)
    profiling_data: Dict[str, Any] = field(default_factory=dict)
    reasoning_traces: List[str] = field(default_factory=list)
    constraint_violations: List[str] = field(default_factory=list)
    visual_feedback: List[str] = field(default_factory=list)
    custom_metrics: Dict[str, float] = field(default_factory=dict)
    
    def add_error(self, error: str):
        """Add an error message"""
        self.error_messages.append(error)
    
    def add_profiling(self, key: str, value: Any):
        """Add profiling data"""
        self.profiling_data[key] = value
    
    def add_reasoning(self, reasoning: str):
        """Add reasoning trace"""
        self.reasoning_traces.append(reasoning)
    
    def add_constraint_violation(self, violation: str):
        """Add constraint violation"""
        self.constraint_violations.append(violation)
    
    def add_visual_feedback(self, feedback: str):
        """Add visual feedback"""
        self.visual_feedback.append(feedback)
    
    def add_metric(self, key: str, value: float):
        """Add custom metric"""
        self.custom_metrics[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_messages": self.error_messages,
            "profiling_data": self.profiling_data,
            "reasoning_traces": self.reasoning_traces,
            "constraint_violations": self.constraint_violations,
            "visual_feedback": self.visual_feedback,
            "custom_metrics": self.custom_metrics
        }


@dataclass
class DiagnosticInfo:
    """Diagnostic information for skill evaluation"""
    content_analysis: str = ""
    structure_evaluation: str = ""
    gap_identification: List[str] = field(default_factory=list)
    strength_highlighting: List[str] = field(default_factory=list)
    actionable_recommendations: List[str] = field(default_factory=list)


@dataclass
class EvolutionTrace:
    """Trace of an evolution iteration with diagnostic information"""
    success: bool = True
    error_messages: List[str] = field(default_factory=list)
    reasoning_logs: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    improvement_suggestions: List[str] = field(default_factory=list)
    diagnostic_info: Optional[DiagnosticInfo] = None
    asi: Optional[ActionableSideInfo] = None
    
    def add_error(self, error: str):
        """Add an error message"""
        self.error_messages.append(error)
        self.success = False
    
    def add_reasoning(self, reasoning: str):
        """Add reasoning information"""
        self.reasoning_logs.append(reasoning)
    
    def add_metric(self, key: str, value: float):
        """Add a performance metric"""
        self.performance_metrics[key] = value
    
    def add_suggestion(self, suggestion: str):
        """Add an improvement suggestion"""
        self.improvement_suggestions.append(suggestion)
    
    def set_diagnostic(self, diagnostic: DiagnosticInfo):
        """Set diagnostic information"""
        self.diagnostic_info = diagnostic
    
    def set_asi(self, asi: ActionableSideInfo):
        """Set actionable side information"""
        self.asi = asi
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "error_messages": self.error_messages,
            "reasoning_logs": self.reasoning_logs,
            "performance_metrics": self.performance_metrics,
            "improvement_suggestions": self.improvement_suggestions,
            "diagnostic_info": {
                "content_analysis": self.diagnostic_info.content_analysis if self.diagnostic_info else "",
                "structure_evaluation": self.diagnostic_info.structure_evaluation if self.diagnostic_info else "",
                "gap_identification": self.diagnostic_info.gap_identification if self.diagnostic_info else [],
                "strength_highlighting": self.diagnostic_info.strength_highlighting if self.diagnostic_info else [],
                "actionable_recommendations": self.diagnostic_info.actionable_recommendations if self.diagnostic_info else []
            } if self.diagnostic_info else None,
            "asi": self.asi.to_dict() if self.asi else None
        }


@dataclass
class EvolutionCandidate:
    """A candidate skill in the optimization process"""
    content: str
    version: int = 1
    fitness_scores: Dict[EvolutionObjective, float] = field(default_factory=dict)
    trace: Optional[EvolutionTrace] = None
    ancestors: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    knowledge_base: Dict[str, Any] = field(default_factory=dict)
    task_performance: Dict[str, float] = field(default_factory=dict)
    
    @property
    def overall_fitness(self) -> float:
        """Calculate overall fitness as weighted average of objective scores"""
        if not self.fitness_scores:
            return 0.0
        
        weights = {
            EvolutionObjective.READABILITY: 0.20,
            EvolutionObjective.COMPLETENESS: 0.25,
            EvolutionObjective.EFFICIENCY: 0.15,
            EvolutionObjective.ROBUSTNESS: 0.20,
            EvolutionObjective.CLARITY: 0.10,
            EvolutionObjective.USABILITY: 0.10
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for obj, score in self.fitness_scores.items():
            weight = weights.get(obj, 1.0 / len(self.fitness_scores))
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def dominates(self, other: 'EvolutionCandidate') -> bool:
        """Check if this candidate is better than or equal to another in all objectives"""
        if not self.fitness_scores or not other.fitness_scores:
            return False
        
        has_better = False
        for obj in EvolutionObjective:
            self_score = self.fitness_scores.get(obj, 0.0)
            other_score = other.fitness_scores.get(obj, 0.0)
            
            if self_score < other_score:
                return False
            if self_score > other_score:
                has_better = True
        
        return has_better
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "version": self.version,
            "fitness_scores": {obj.value: score for obj, score in self.fitness_scores.items()},
            "trace": self.trace.to_dict() if self.trace else None,
            "ancestors": self.ancestors,
            "created_at": self.created_at,
            "knowledge_base": self.knowledge_base,
            "task_performance": self.task_performance
        }


@dataclass
class EvolutionConfig:
    """Configuration for the evolution process"""
    max_iterations: int = 10
    frontier_size: int = 7
    use_intelligent_reflection: bool = True
    use_knowledge_integration: bool = True
    use_candidate_merge: bool = True
    use_multi_objective: bool = True
    objectives: List[EvolutionObjective] = field(default_factory=lambda: list(EvolutionObjective))
    model: str = "openai/gpt-5.4"
    reflection_depth: int = 3
    minibatch_size: int = 3
    use_system_aware_merge: bool = True
    use_curriculum_learning: bool = True
    use_goal_oriented_evolution: bool = True
    use_self_verification: bool = True
    use_meta_cognition: bool = True
    mutation_rate: float = 0.3
    crossover_rate: float = 0.4
    adaptive_mutation: bool = True
    current_curriculum_level: int = 0
    success_threshold_for_level_up: float = 0.8
    max_curriculum_level: int = 5


class EvolutionEngine:
    """
    Octopai's Evolution Engine - Advanced Skill Evolution System.
    
    Provides sophisticated skill optimization through Octopai's proprietary
    multi-objective evolutionary algorithm with intelligent reflection,
    knowledge integration, and iterative refinement. Features a three-stage
    pipeline: Executor, Reflector, and Optimizer.

    Skills continuously learn from interactions, refine through reflection,
    and evolve to become more powerful and better suited to AI Agent needs.

    Key Principles:
    - Skills Evolve Through Continuous Learning
    - Every Interaction Feeds Future Improvements
    - Knowledge Accumulates Across Generations
    - AI Agent Cognition Elevates Over Time
    - Curriculum-Based Learning Progression
    - Goal-Oriented Evolution
    - Self-Verification and Validation
    - Meta-Cognitive Process Optimization
    """

    def __init__(self, config: Optional[EvolutionConfig] = None, experience_tracker=None):
        self.config = config or EvolutionConfig()
        self.api_config = Config()
        self.candidate_frontier: List[EvolutionCandidate] = []
        self.evolution_history: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.knowledge_chunks: List[KnowledgeChunk] = []
        self.lessons_learned: List[str] = []
        self.reflection_archive: List[Dict[str, Any]] = []
        self.evaluator: Optional[Callable[[str, Any], tuple[float, ActionableSideInfo]]] = None
        self.experience_tracker = experience_tracker
        self.evolution_goals: List[EvolutionGoal] = []
        self.curriculum_levels: List[CurriculumLevel] = self._initialize_curriculum()
        self.meta_cognitive_reflections: List[MetaCognitiveReflection] = []
        self.self_verification_results: List[SelfVerificationResult] = []
        self.performance_trajectory: List[Dict[str, float]] = []
        self.strategy_adaptation_count: int = 0

    def _call_api(self, data: Dict[str, Any], default_response: str = "") -> Optional[str]:
        """Make API call with proper error handling and response parsing"""
        headers = {
            'Authorization': f'Bearer {self.api_config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                self.api_config.OPENROUTER_API_URL,
                headers=headers,
                json=data,
                timeout=90
            )
            response.raise_for_status()
            result = response.json()
            choices = result.get('choices', [])
            if not choices:
                return default_response
            message = choices[0].get('message', {})
            content = message.get('content', '')
            return content if content else default_response
        except requests.exceptions.Timeout:
            print(f"API request timed out")
            return default_response
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            return default_response
        except (ValueError, KeyError) as e:
            print(f"API response parsing failed: {str(e)}")
            return default_response
        except Exception as e:
            print(f"Unexpected API error: {str(e)}")
            return default_response
    
    def _initialize_curriculum(self) -> List[CurriculumLevel]:
        """Initialize a progressive learning curriculum"""
        return [
            CurriculumLevel(
                level=0,
                name="Foundational",
                difficulty=0.2,
                task_complexity=0.2,
                required_success_rate=0.6,
                tasks=[{"type": "basic_validation", "complexity": "low"}]
            ),
            CurriculumLevel(
                level=1,
                name="Structural",
                difficulty=0.4,
                task_complexity=0.4,
                required_success_rate=0.7,
                tasks=[{"type": "structure_validation", "complexity": "medium"}]
            ),
            CurriculumLevel(
                level=2,
                name="Completeness",
                difficulty=0.6,
                task_complexity=0.6,
                required_success_rate=0.75,
                tasks=[{"type": "completeness_validation", "complexity": "medium"}]
            ),
            CurriculumLevel(
                level=3,
                name="Optimization",
                difficulty=0.75,
                task_complexity=0.75,
                required_success_rate=0.8,
                tasks=[{"type": "optimization_validation", "complexity": "high"}]
            ),
            CurriculumLevel(
                level=4,
                name="Advanced",
                difficulty=0.9,
                task_complexity=0.85,
                required_success_rate=0.85,
                tasks=[{"type": "advanced_validation", "complexity": "very_high"}]
            )
        ]
    
    def add_evolution_goal(self, description: str, priority: GoalPriority = GoalPriority.MEDIUM, 
                           success_criteria: str = "") -> EvolutionGoal:
        """Add a specific goal for the evolution process"""
        import uuid
        goal = EvolutionGoal(
            description=description,
            priority=priority,
            success_criteria=success_criteria
        )
        self.evolution_goals.append(goal)
        return goal
    
    def _check_goal_progress(self, candidate: EvolutionCandidate) -> None:
        """Check progress toward evolution goals"""
        for goal in self.evolution_goals:
            if goal.achieved:
                continue
            for obj, score in candidate.fitness_scores.items():
                if obj.value in goal.success_criteria.lower():
                    goal.progress_metrics[obj.value] = score
            if all(score >= 0.8 for score in goal.progress_metrics.values()):
                goal.achieved = True
    
    def _update_curriculum_level(self, success_rate: float) -> None:
        """Update curriculum level based on performance"""
        if not self.config.use_curriculum_learning:
            return
        
        current_level = self.curriculum_levels[self.config.current_curriculum_level]
        
        if success_rate >= current_level.required_success_rate:
            if self.config.current_curriculum_level < self.config.max_curriculum_level:
                self.config.current_curriculum_level += 1
                print(f"  Advanced to curriculum level {self.config.current_curriculum_level}: {self.curriculum_levels[self.config.current_curriculum_level].name}")
        elif success_rate < current_level.required_success_rate * 0.7:
            if self.config.current_curriculum_level > 0:
                self.config.current_curriculum_level -= 1
                print(f"  Regressed to curriculum level {self.config.current_curriculum_level}: {self.curriculum_levels[self.config.current_curriculum_level].name}")
    
    def _self_verify(self, candidate: EvolutionCandidate) -> SelfVerificationResult:
        """Perform self-verification of a candidate"""
        import uuid
        verification_id = str(uuid.uuid4())
        result = SelfVerificationResult(verification_id=verification_id)
        
        if not self.config.use_self_verification:
            result.passed = True
            result.confidence_score = 0.5
            return result
        
        try:
            content = candidate.content
            
            result.test_results["has_structure"] = "##" in content
            result.test_results["has_examples"] = "example" in content.lower() or "Example" in content
            result.test_results["has_troubleshooting"] = "troubleshoot" in content.lower() or "Troubleshoot" in content
            result.test_results["has_best_practices"] = "best practice" in content.lower() or "Best Practice" in content
            result.test_results["has_code_blocks"] = content.count('```') >= 2
            
            passed_tests = sum(1 for passed in result.test_results.values() if passed)
            result.confidence_score = passed_tests / len(result.test_results)
            result.passed = result.confidence_score >= 0.6
            
            if not result.passed:
                for test_name, passed in result.test_results.items():
                    if not passed:
                        result.issues_found.append(f"Failed test: {test_name}")
                        result.recommendations.append(f"Improve: {test_name.replace('_', ' ')}")
            
        except Exception as e:
            result.issues_found.append(f"Verification error: {str(e)}")
            result.confidence_score = 0.0
            result.passed = False
        
        self.self_verification_results.append(result)
        return result
    
    def _meta_cognitive_reflect(self, iteration: int, traces: List[EvolutionTrace]) -> MetaCognitiveReflection:
        """Perform meta-cognitive reflection on the evolution process"""
        import uuid
        reflection = MetaCognitiveReflection(reflection_id=str(uuid.uuid4()))
        
        if not self.config.use_meta_cognition:
            return reflection
        
        if len(self.performance_trajectory) >= 3:
            recent_performance = self.performance_trajectory[-3:]
            avg_fitness = sum(p.get('avg_fitness', 0) for p in recent_performance) / len(recent_performance)
            fitness_trend = recent_performance[-1].get('avg_fitness', 0) - recent_performance[0].get('avg_fitness', 0)
            
            if fitness_trend < -0.1:
                reflection.process_insights.append("Performance is declining - consider strategy adjustment")
                reflection.strategy_adjustments.append("Increase mutation rate for exploration")
                reflection.learning_rate_optimization['mutation_rate'] = min(0.6, self.config.mutation_rate + 0.1)
            elif fitness_trend > 0.1:
                reflection.process_insights.append("Performance is improving - current strategy effective")
                reflection.learning_rate_optimization['mutation_rate'] = max(0.1, self.config.mutation_rate - 0.05)
            else:
                reflection.process_insights.append("Performance stable - maintaining current strategy")
            
            if avg_fitness > 0.8:
                reflection.pattern_recognitions.append("High fitness achieved - focusing on refinement")
            elif avg_fitness < 0.5:
                reflection.pattern_recognitions.append("Low fitness - exploring new approaches")
        
        if iteration % self.config.reflection_depth == 0 and iteration > 0:
            reflection.process_insights.append("Regular meta-cognitive check point")
        
        self.meta_cognitive_reflections.append(reflection)
        
        if reflection.learning_rate_optimization and self.config.adaptive_mutation:
            if 'mutation_rate' in reflection.learning_rate_optimization:
                self.config.mutation_rate = reflection.learning_rate_optimization['mutation_rate']
                self.strategy_adaptation_count += 1
        
        return reflection
    
    def _adaptive_mutation(self, candidate: EvolutionCandidate, diagnosis: str) -> EvolutionCandidate:
        """Apply adaptive mutation based on current state"""
        mutation_strategy = "reflective"
        
        if self.config.adaptive_mutation:
            if len(self.performance_trajectory) >= 2:
                last_fitness = self.performance_trajectory[-1].get('avg_fitness', 0) if self.performance_trajectory else 0
                prev_fitness = self.performance_trajectory[-2].get('avg_fitness', 0) if len(self.performance_trajectory) >= 2 else 0
                
                if last_fitness - prev_fitness < -0.05:
                    mutation_strategy = "exploratory"
                elif last_fitness > 0.85:
                    mutation_strategy = "refinement"
        
        return self._mutate_by_strategy(candidate, diagnosis, mutation_strategy)
    
    def _mutate_by_strategy(self, candidate: EvolutionCandidate, diagnosis: str, strategy: str) -> EvolutionCandidate:
        """Apply mutation based on specified strategy"""
        if strategy == "exploratory":
            return self._exploratory_mutation(candidate, diagnosis)
        elif strategy == "refinement":
            return self._refinement_mutation(candidate, diagnosis)
        else:
            return self._reflective_mutation(candidate, diagnosis)
    
    def _exploratory_mutation(self, candidate: EvolutionCandidate, diagnosis: str) -> EvolutionCandidate:
        """Exploratory mutation for discovering new approaches"""
        lessons_text = "\n".join([f"- {lesson}" for lesson in self.lessons_learned[-10:]])
        
        headers = {
            'Authorization': f'Bearer {self.api_config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at creative skill evolution and exploration.
Create a significantly different version that explores new approaches and structures.
Be bold and creative while maintaining quality.
Focus on:
1. Exploring alternative structures
2. Trying new organization patterns
3. Experimenting with different content styles
4. Adding innovative sections and elements"""
                },
                {
                    "role": "user",
                    "content": f"""Current skill (v{candidate.version}):
{candidate.content}

Diagnosis:
{diagnosis}

Lessons Learned:
{lessons_text}

Please create an exploratory, innovative version (v{candidate.version + 1}) that explores new approaches."""
                }
            ],
            "temperature": 0.9
        }
        
        try:
            improved_content = self._call_api(data, candidate.content)

            new_knowledge = candidate.knowledge_base.copy()
            new_knowledge[f'v{candidate.version}_exploratory'] = {'strategy': 'exploratory', 'timestamp': datetime.now().isoformat()}

            return EvolutionCandidate(
                content=improved_content,
                version=candidate.version + 1,
                ancestors=candidate.ancestors + [f"v{candidate.version}_exploratory"],
                knowledge_base=new_knowledge
            )

        except Exception as e:
            print(f"Exploratory mutation failed: {e}")
            return candidate

    def _refinement_mutation(self, candidate: EvolutionCandidate, diagnosis: str) -> EvolutionCandidate:
        """Refinement mutation for polishing high-quality candidates"""
        lessons_text = "\n".join([f"- {lesson}" for lesson in self.lessons_learned[-20:]])

        data = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at skill refinement and polish.
Take a high-quality skill and make it exceptional through careful refinement.
Focus on:
1. Perfecting existing content
2. Enhancing clarity and precision
3. Adding fine details and nuance
4. Ensuring consistency and flow
5. Polishing examples and explanations"""
                },
                {
                    "role": "user",
                    "content": f"""Current skill (v{candidate.version}):
{candidate.content}

Diagnosis:
{diagnosis}

Lessons Learned:
{lessons_text}

Please create a refined, polished version (v{candidate.version + 1}) that perfects the existing content."""
                }
            ],
            "temperature": 0.4
        }
        
        try:
            improved_content = self._call_api(data, candidate.content)

            new_knowledge = candidate.knowledge_base.copy()
            new_knowledge[f'v{candidate.version}_refinement'] = {'strategy': 'refinement', 'timestamp': datetime.now().isoformat()}

            return EvolutionCandidate(
                content=improved_content,
                version=candidate.version + 1,
                ancestors=candidate.ancestors + [f"v{candidate.version}_refinement"],
                knowledge_base=new_knowledge
            )

        except Exception as e:
            print(f"Refinement mutation failed: {e}")
            return candidate

    def _add_knowledge_chunk(self, content: str, source: str, category: str, relevance_score: float = 0.5) -> str:
        """Add a chunk of knowledge to the knowledge base"""
        import uuid
        chunk_id = str(uuid.uuid4())
        chunk = KnowledgeChunk(
            chunk_id=chunk_id,
            content=content,
            source=source,
            relevance_score=relevance_score,
            category=category
        )
        self.knowledge_chunks.append(chunk)
        
        if len(self.knowledge_chunks) > 500:
            self.knowledge_chunks.sort(key=lambda c: c.relevance_score, reverse=True)
            self.knowledge_chunks = self.knowledge_chunks[:500]
        
        return chunk_id
    
    def _retrieve_relevant_knowledge(self, query: str, limit: int = 5) -> List[KnowledgeChunk]:
        """Retrieve relevant knowledge chunks based on query"""
        query_lower = query.lower()
        
        scored_chunks = []
        for chunk in self.knowledge_chunks:
            score = 0.0
            if query_lower in chunk.content.lower():
                score += 0.5
            score += chunk.relevance_score * 0.3
            if chunk.last_accessed:
                days_since = (datetime.now() - datetime.fromisoformat(chunk.last_accessed)).days
                score += max(0, 0.2 - (days_since * 0.01))
            scored_chunks.append((score, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        for _, chunk in scored_chunks[:limit]:
            chunk.access_count += 1
            chunk.last_accessed = datetime.now().isoformat()
        
        return [chunk for _, chunk in scored_chunks[:limit]]
    
    def evolve_skill(
        self,
        skill_dir: str,
        config: Optional[EvolutionConfig] = None,
        evaluator: Optional[Callable[[str, Any], tuple[float, ActionableSideInfo]]] = None,
        evaluation_tasks: Optional[List[Any]] = None
    ) -> str:
        """
        Evolve a skill through Octopai's evolutionary process
        
        Args:
            skill_dir: Directory containing the skill to evolve
            config: Optional evolution configuration
            evaluator: Optional custom evaluator function
            evaluation_tasks: Optional list of evaluation tasks
            
        Returns:
            Path to the evolved skill directory
        """
        if config:
            self.config = config
        
        if evaluator:
            self.evaluator = evaluator
        
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_file):
            raise Exception(f"SKILL.md not found: {skill_file}")
        
        initial_content = read_file(skill_file)
        initial_candidate = EvolutionCandidate(content=initial_content)
        
        self.candidate_frontier = [initial_candidate]
        self.evolution_history = []
        self.knowledge_base = {}
        
        if self.experience_tracker:
            skill_id = os.path.basename(skill_dir)
            skill_experience = self.experience_tracker.get_skill_experience(skill_id)
            if skill_experience:
                self._integrate_experience_into_knowledge(skill_experience)
        
        print(f"Starting evolution with {self.config.max_iterations} iterations...")
        
        if self.config.use_curriculum_learning:
            print(f"  Initial curriculum level: {self.config.current_curriculum_level} - {self.curriculum_levels[self.config.current_curriculum_level].name}")
        
        for iteration in range(self.config.max_iterations):
            print(f"\nIteration {iteration + 1}/{self.config.max_iterations}")
            
            traces = self._execute_candidates(evaluation_tasks)
            
            if self.config.use_intelligent_reflection:
                self._reflect_on_traces(traces, iteration)
            
            if self.config.use_meta_cognition:
                meta_reflection = self._meta_cognitive_reflect(iteration, traces)
                if meta_reflection.process_insights:
                    print(f"  Meta-cognitive insights: {len(meta_reflection.process_insights)}")
            
            diagnosis = self._synthesize_diagnosis(traces)
            self._extract_knowledge(diagnosis)
            
            if self.config.use_goal_oriented_evolution:
                for candidate in self.candidate_frontier:
                    self._check_goal_progress(candidate)
            
            new_candidates = self._mutate_candidates(diagnosis)
            
            if self.config.use_system_aware_merge and len(new_candidates) >= 2:
                merged = self._system_aware_merge(new_candidates)
                new_candidates.extend(merged)
            
            if self.config.use_self_verification:
                verified_candidates = []
                for candidate in new_candidates:
                    verification = self._self_verify(candidate)
                    if verification.passed or verification.confidence_score >= 0.5:
                        verified_candidates.append(candidate)
                if verified_candidates:
                    new_candidates = verified_candidates
                    print(f"  Self-verification: {len(verified_candidates)}/{len(new_candidates) + len(verified_candidates) - len(verified_candidates)} candidates passed")
            
            self._update_pareto_frontier(new_candidates)
            
            if self.config.use_curriculum_learning and self.candidate_frontier:
                avg_fitness = sum(c.overall_fitness for c in self.candidate_frontier) / len(self.candidate_frontier)
                self._update_curriculum_level(avg_fitness)
            
            self._record_iteration(iteration, traces, diagnosis, new_candidates)
            
            if self.candidate_frontier:
                avg_fitness = sum(c.overall_fitness for c in self.candidate_frontier) / len(self.candidate_frontier)
                self.performance_trajectory.append({
                    'iteration': iteration + 1,
                    'avg_fitness': avg_fitness,
                    'best_fitness': max(c.overall_fitness for c in self.candidate_frontier),
                    'curriculum_level': self.config.current_curriculum_level
                })
        
        best_candidate = self._select_best_candidate()
        write_file(skill_file, best_candidate.content)
        self._save_evolution_history(skill_dir, best_candidate)
        
        print(f"\nEvolution complete! Best fitness: {best_candidate.overall_fitness:.2f}")
        
        return skill_dir
    
    def _execute_candidates(self, tasks: Optional[List[Any]] = None) -> List[EvolutionTrace]:
        """Stage 1: Executor - Run candidates and capture traces"""
        traces = []
        
        for candidate in self.candidate_frontier:
            trace = self._execute_candidate(candidate, tasks)
            candidate.trace = trace
            self._calculate_fitness(candidate, trace)
            traces.append(trace)
        
        return traces
    
    def _execute_candidate(
        self, 
        candidate: EvolutionCandidate, 
        tasks: Optional[List[Any]] = None
    ) -> EvolutionTrace:
        """Execute a single candidate and capture execution trace"""
        trace = EvolutionTrace()
        asi = ActionableSideInfo()
        
        try:
            if self.evaluator and tasks:
                for task in tasks[:self.config.minibatch_size]:
                    try:
                        score, candidate_asi = self.evaluator(candidate.content, task)
                        candidate.task_performance[str(task)] = score
                        
                        asi.error_messages.extend(candidate_asi.error_messages)
                        asi.profiling_data.update(candidate_asi.profiling_data)
                        asi.reasoning_traces.extend(candidate_asi.reasoning_traces)
                        asi.constraint_violations.extend(candidate_asi.constraint_violations)
                    except Exception as e:
                        asi.add_error(str(e))
            else:
                content_length = len(candidate.content)
                has_structure = "##" in candidate.content or "###" in candidate.content
                has_examples = "example" in candidate.content.lower() or "Example" in candidate.content
                has_troubleshooting = "troubleshoot" in candidate.content.lower() or "Troubleshoot" in candidate.content
                has_best_practices = "best practice" in candidate.content.lower() or "Best Practice" in candidate.content
                
                readability_score = self._calculate_readability(candidate.content)
                completeness_score = self._calculate_completeness(candidate.content)
                clarity_score = self._calculate_clarity(candidate.content)
                efficiency_score = 0.7 + 0.1 * (content_length > 300)
                robustness_score = 0.65 + 0.15 * has_troubleshooting
                usability_score = 0.6 + 0.2 * has_examples + 0.1 * has_best_practices
                
                asi.add_metric(EvolutionObjective.READABILITY.value, readability_score)
                asi.add_metric(EvolutionObjective.COMPLETENESS.value, completeness_score)
                asi.add_metric(EvolutionObjective.CLARITY.value, clarity_score)
                asi.add_metric(EvolutionObjective.EFFICIENCY.value, efficiency_score)
                asi.add_metric(EvolutionObjective.ROBUSTNESS.value, robustness_score)
                asi.add_metric(EvolutionObjective.USABILITY.value, usability_score)
                
                trace.add_metric(EvolutionObjective.READABILITY.value, readability_score)
                trace.add_metric(EvolutionObjective.COMPLETENESS.value, completeness_score)
                trace.add_metric(EvolutionObjective.CLARITY.value, clarity_score)
                trace.add_metric(EvolutionObjective.EFFICIENCY.value, efficiency_score)
                trace.add_metric(EvolutionObjective.ROBUSTNESS.value, robustness_score)
                trace.add_metric(EvolutionObjective.USABILITY.value, usability_score)
                
                if not has_structure:
                    trace.add_suggestion("Add section headers for better organization and navigation")
                if not has_examples:
                    trace.add_suggestion("Include practical examples to demonstrate usage patterns")
                if not has_troubleshooting:
                    trace.add_suggestion("Add troubleshooting guidance for common issues")
                if not has_best_practices:
                    trace.add_suggestion("Include best practices and recommendations")
            
            trace.success = True
            trace.add_reasoning("Candidate executed successfully with comprehensive analysis")
            trace.set_asi(asi)
            
        except Exception as e:
            trace.success = False
            trace.add_error(str(e))
            asi.add_error(str(e))
            trace.set_asi(asi)
        
        return trace
    
    def _reflect_on_traces(self, traces: List[EvolutionTrace], iteration: int):
        """Stage 2: Reflector - Analyze traces to understand failure modes"""
        if iteration % self.config.reflection_depth != 0:
            return
        
        print("  Performing intelligent reflection...")
        
        for i, trace in enumerate(traces):
            diagnostic = self._generate_diagnostic(trace, i)
            trace.set_diagnostic(diagnostic)
            
            reflection_record = {
                "iteration": iteration,
                "candidate_index": i,
                "diagnostic": {
                    "content_analysis": diagnostic.content_analysis,
                    "gap_identification": diagnostic.gap_identification,
                    "strength_highlighting": diagnostic.strength_highlighting,
                    "actionable_recommendations": diagnostic.actionable_recommendations
                },
                "timestamp": datetime.now().isoformat()
            }
            self.reflection_archive.append(reflection_record)
            
            for recommendation in diagnostic.actionable_recommendations:
                if recommendation not in self.lessons_learned:
                    self.lessons_learned.append(recommendation)
    
    def _mutate_candidates(self, diagnosis: str) -> List[EvolutionCandidate]:
        """Stage 3: Optimizer - Generate improved candidates based on insights"""
        new_candidates = []
        
        for candidate in self.candidate_frontier:
            if self.config.adaptive_mutation:
                improved = self._adaptive_mutation(candidate, diagnosis)
            else:
                improved = self._reflective_mutation(candidate, diagnosis)
            new_candidates.append(improved)
        
        return new_candidates
    
    def _reflective_mutation(self, candidate: EvolutionCandidate, diagnosis: str) -> EvolutionCandidate:
        """Generate an improved version using reflective mutation"""
        lessons_text = "\n".join([f"- {lesson}" for lesson in self.lessons_learned[-15:]])
        
        knowledge_context = ""
        if self.config.use_knowledge_integration and candidate.knowledge_base:
            knowledge_context = f"\n\nCandidate Knowledge Base:\n{json.dumps(candidate.knowledge_base, indent=2)}"
        
        asi_context = ""
        if candidate.trace and candidate.trace.asi:
            asi_context = f"\n\nActionable Side Information:\n{json.dumps(candidate.trace.asi.to_dict(), indent=2)}"
        
        headers = {
            'Authorization': f'Bearer {self.api_config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at skill improvement and evolution.
Create an improved version based on the diagnosis, accumulated lessons, and actionable side information.
Make targeted, meaningful improvements while preserving what works well.
Focus on:
1. Addressing identified gaps
2. Building on existing strengths
3. Applying learned lessons
4. Resolving issues from actionable side information
5. Enhancing structure and clarity
6. Adding practical examples and guidance"""
                },
                {
                    "role": "user",
                    "content": f"""Current skill (v{candidate.version}):
{candidate.content}

Comprehensive Diagnosis:
{diagnosis}

Accumulated Lessons:
{lessons_text}{knowledge_context}{asi_context}

Please create an improved version (v{candidate.version + 1})."""
                }
            ],
            "temperature": 0.65
        }
        
        try:
            improved_content = self._call_api(data, candidate.content)

            new_knowledge = candidate.knowledge_base.copy()
            new_knowledge[f'v{candidate.version}_improvements'] = {
                'applied_lessons': self.lessons_learned[-5:],
                'timestamp': datetime.now().isoformat()
            }

            return EvolutionCandidate(
                content=improved_content,
                version=candidate.version + 1,
                ancestors=candidate.ancestors + [f"v{candidate.version}"],
                knowledge_base=new_knowledge
            )

        except Exception as e:
            print(f"Reflective mutation failed: {e}")
            return candidate

    def _system_aware_merge(self, candidates: List[EvolutionCandidate]) -> List[EvolutionCandidate]:
        """System-aware merge of complementary candidates"""
        merged_candidates = []
        
        if len(candidates) < 2:
            return merged_candidates
        
        for i in range(min(3, len(candidates) - 1)):
            for j in range(i + 1, min(i + 2, len(candidates))):
                merged = self._merge_pair_system_aware(candidates[i], candidates[j])
                if merged:
                    merged_candidates.append(merged)
        
        return merged_candidates
    
    def _merge_pair_system_aware(
        self, 
        candidate_a: EvolutionCandidate, 
        candidate_b: EvolutionCandidate
    ) -> Optional[EvolutionCandidate]:
        """Merge a pair of candidates with system awareness"""
        headers = {
            'Authorization': f'Bearer {self.api_config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        a_strengths = [obj.value for obj, score in candidate_a.fitness_scores.items() if score > 0.75]
        b_strengths = [obj.value for obj, score in candidate_b.fitness_scores.items() if score > 0.75]
        
        data = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert at skill composition and integration.
Combine the strengths of two skills into one superior skill through system-aware merging.
Identify and integrate:
1. Unique strengths from each candidate
2. Complementary structural elements
3. Best practices from both versions
4. Comprehensive coverage of topics
5. Enhanced usability and clarity
6. System-consistent architecture and patterns"""
                },
                {
                    "role": "user",
                    "content": f"""Candidate A (v{candidate_a.version}) - Strengths: {', '.join(a_strengths)}:
{candidate_a.content}

Candidate B (v{candidate_b.version}) - Strengths: {', '.join(b_strengths)}:
{candidate_b.content}

Please merge these two skills, combining their unique strengths through system-aware integration and creating a superior version."""
                }
            ],
            "temperature": 0.6
        }
        
        try:
            merged_content = self._call_api(data, candidate_a.content)

            combined_knowledge = {}
            combined_knowledge.update(candidate_a.knowledge_base)
            combined_knowledge.update(candidate_b.knowledge_base)
            combined_knowledge['merge_source'] = f"v{candidate_a.version}+v{candidate_b.version}"
            combined_knowledge['merge_type'] = "system_aware"

            return EvolutionCandidate(
                content=merged_content,
                version=max(candidate_a.version, candidate_b.version) + 1,
                ancestors=[f"system_aware_merge(v{candidate_a.version}+v{candidate_b.version})"],
                knowledge_base=combined_knowledge
            )

        except Exception as e:
            print(f"System-aware merge failed: {e}")
            return None

    def _update_pareto_frontier(self, new_candidates: List[EvolutionCandidate]):
        """Update the Pareto frontier with new candidates"""
        for candidate in new_candidates:
            trace = self._execute_candidate(candidate)
            candidate.trace = trace
            self._calculate_fitness(candidate, trace)
            
            should_add = True
            to_remove = []
            
            for existing in self.candidate_frontier:
                if existing.dominates(candidate):
                    should_add = False
                    break
                if candidate.dominates(existing):
                    to_remove.append(existing)
            
            if should_add:
                for remove_candidate in to_remove:
                    self.candidate_frontier.remove(remove_candidate)
                
                self.candidate_frontier.append(candidate)
                
                if len(self.candidate_frontier) > self.config.frontier_size:
                    self.candidate_frontier.sort(
                        key=lambda c: c.overall_fitness,
                        reverse=True
                    )
                    self.candidate_frontier = self.candidate_frontier[:self.config.frontier_size]
    
    def _calculate_readability(self, content: str) -> float:
        """Calculate readability score based on content structure"""
        score = 0.5
        lines = content.split('\n')
        
        if any(line.startswith('#') for line in lines):
            score += 0.15
        if any(line.startswith('##') for line in lines):
            score += 0.1
        if any(line.startswith('###') for line in lines):
            score += 0.1
        if len(lines) > 10 and len(lines) < 500:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_completeness(self, content: str) -> float:
        """Calculate completeness score based on content coverage"""
        score = 0.4
        content_lower = content.lower()
        
        if 'overview' in content_lower or 'introduction' in content_lower:
            score += 0.1
        if 'usage' in content_lower or 'example' in content_lower:
            score += 0.15
        if 'best practice' in content_lower or 'recommendation' in content_lower:
            score += 0.1
        if 'troubleshoot' in content_lower or 'faq' in content_lower:
            score += 0.1
        if 'configuration' in content_lower or 'setup' in content_lower:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_clarity(self, content: str) -> float:
        """Calculate clarity score based on content quality"""
        score = 0.5
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['note:', 'important:', 'warning:']):
            score += 0.1
        if len(content) > 500:
            score += 0.1
        if content.count('```') >= 2:
            score += 0.15
        if content.count('- ') > 3 or content.count('* ') > 3:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_fitness(self, candidate: EvolutionCandidate, trace: EvolutionTrace):
        """Calculate fitness scores from evaluation trace"""
        for obj in EvolutionObjective:
            if obj.value in trace.performance_metrics:
                candidate.fitness_scores[obj] = trace.performance_metrics[obj.value]
    
    def _generate_diagnostic(self, trace: EvolutionTrace, candidate_index: int) -> DiagnosticInfo:
        """Generate comprehensive diagnostic information"""
        diagnostic = DiagnosticInfo()
        
        metric_summary = json.dumps(trace.performance_metrics, indent=2)
        
        diagnostic.content_analysis = f"Candidate {candidate_index + 1} performance metrics: {metric_summary}"
        diagnostic.structure_evaluation = "Structural analysis complete"
        
        for suggestion in trace.improvement_suggestions:
            diagnostic.gap_identification.append(suggestion)
        
        for obj, score in [(obj, trace.performance_metrics.get(obj.value, 0)) 
                          for obj in EvolutionObjective 
                          if trace.performance_metrics.get(obj.value, 0) > 0.7]:
            diagnostic.strength_highlighting.append(f"Strong performance in {obj.value}: {score:.2f}")
        
        diagnostic.actionable_recommendations = trace.improvement_suggestions.copy()
        
        return diagnostic
    
    def _synthesize_diagnosis(self, traces: List[EvolutionTrace]) -> str:
        """Synthesize comprehensive diagnosis from all traces"""
        analysis_parts = []
        
        for i, trace in enumerate(traces):
            candidate_info = f"Candidate {i+1}:\n"
            candidate_info += f"  Success: {trace.success}\n"
            candidate_info += f"  Errors: {', '.join(trace.error_messages) if trace.error_messages else 'None'}\n"
            candidate_info += f"  Metrics: {json.dumps(trace.performance_metrics, indent=4)}\n"
            candidate_info += f"  Suggestions: {', '.join(trace.improvement_suggestions) if trace.improvement_suggestions else 'None'}\n"
            
            if trace.asi:
                candidate_info += f"  ASI Errors: {', '.join(trace.asi.error_messages) if trace.asi.error_messages else 'None'}\n"
                candidate_info += f"  ASI Profiling: {json.dumps(trace.asi.profiling_data, indent=4)}\n"
            
            if trace.diagnostic_info:
                candidate_info += f"  Strengths: {', '.join(trace.diagnostic_info.strength_highlighting)}\n"
                candidate_info += f"  Recommendations: {', '.join(trace.diagnostic_info.actionable_recommendations)}\n"
            
            analysis_parts.append(candidate_info)
        
        trace_analysis = "\n".join(analysis_parts)
        
        knowledge_summary = "\n".join([f"- {lesson}" for lesson in self.lessons_learned[-15:]])
        
        headers = {
            'Authorization': f'Bearer {self.api_config.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert in skill optimization and continuous improvement.
Analyze the evaluation traces, actionable side information, and accumulated knowledge to:
1. Identify patterns and recurring themes across candidates
2. Extract actionable, targeted improvements
3. Synthesize comprehensive recommendations
4. Suggest how to combine complementary strengths
5. Prioritize improvements based on impact potential"""
                },
                {
                    "role": "user",
                    "content": f"""Evaluation Traces:
{trace_analysis}

Accumulated Knowledge:
{knowledge_summary}

Please provide comprehensive diagnosis and prioritized recommendations."""
                }
            ],
            "temperature": 0.6
        }
        
        try:
            return self._call_api(data, "No diagnosis available")
        except Exception as e:
            return f"Analysis synthesis: {str(e)}"
    
    def _extract_knowledge(self, diagnosis: str):
        """Extract and integrate knowledge from diagnosis"""
        lines = diagnosis.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('*') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                lesson = line.lstrip('-*123456789. ').strip()
                if lesson and lesson not in self.lessons_learned:
                    self.lessons_learned.append(lesson)
        
        if len(self.lessons_learned) > 100:
            self.lessons_learned = self.lessons_learned[-100:]
        
        self.knowledge_base['recent_lessons'] = self.lessons_learned[-20:]
        self.knowledge_base['total_lessons'] = len(self.lessons_learned)
    
    def _integrate_experience_into_knowledge(self, skill_experience):
        """Integrate accumulated experience data into the knowledge base for evolution"""
        self.knowledge_base['experience_summary'] = {
            'total_interactions': skill_experience.total_interactions,
            'success_rate': skill_experience.success_rate,
            'average_duration': skill_experience.average_duration,
            'most_recent_use': skill_experience.most_recent_use
        }
        
        if skill_experience.common_errors:
            for error in skill_experience.common_errors:
                lesson = f"Address frequent issue: {error}"
                if lesson not in self.lessons_learned:
                    self.lessons_learned.append(lesson)
        
        if skill_experience.improvement_suggestions:
            for suggestion in skill_experience.improvement_suggestions:
                if suggestion not in self.lessons_learned:
                    self.lessons_learned.append(suggestion)
        
        if skill_experience.version_stats:
            version_performance = []
            for version, stats in skill_experience.version_stats.items():
                if stats['count'] > 0:
                    success_rate = stats['successes'] / stats['count']
                    version_performance.append((version, success_rate, stats['count']))
            
            version_performance.sort(key=lambda x: x[1], reverse=True)
            for version, success_rate, count in version_performance[:3]:
                lesson = f"Version {version} demonstrated {success_rate:.1%} success rate over {count} uses"
                if lesson not in self.lessons_learned:
                    self.lessons_learned.append(lesson)
        
        if skill_experience.top_performance_metrics:
            self.knowledge_base['historical_metrics'] = skill_experience.top_performance_metrics
    
    def _select_best_candidate(self) -> EvolutionCandidate:
        """Select the best candidate from the frontier"""
        if not self.candidate_frontier:
            raise ValueError("No candidates available")
        return max(self.candidate_frontier, key=lambda c: c.overall_fitness)
    
    def _record_iteration(
        self,
        iteration: int,
        traces: List[EvolutionTrace],
        diagnosis: str,
        new_candidates: List[EvolutionCandidate]
    ):
        """Record iteration history with comprehensive data"""
        record = {
            "iteration": iteration + 1,
            "timestamp": datetime.now().isoformat(),
            "diagnosis": diagnosis,
            "frontier_size": len(self.candidate_frontier),
            "knowledge_base_size": len(self.lessons_learned),
            "candidates": [c.to_dict() for c in new_candidates],
            "reflection_used": self.config.use_intelligent_reflection,
            "knowledge_integration": self.config.use_knowledge_integration
        }
        self.evolution_history.append(record)
    
    def _save_evolution_history(self, skill_dir: str, best_candidate: EvolutionCandidate):
        """Save comprehensive evolution history to disk"""
        history_dir = os.path.join(skill_dir, 'references')
        os.makedirs(history_dir, exist_ok=True)
        
        history_file = os.path.join(history_dir, 'evolution_history.json')
        history = {
            "initial_version": 1,
            "final_version": best_candidate.version,
            "iterations": self.config.max_iterations,
            "best_fitness": best_candidate.overall_fitness,
            "best_candidate": best_candidate.to_dict(),
            "frontier": [c.to_dict() for c in self.candidate_frontier],
            "knowledge_base": self.knowledge_base,
            "knowledge_chunks": [chunk.to_dict() for chunk in self.knowledge_chunks[-50:]],
            "lessons_learned": self.lessons_learned,
            "reflection_archive": self.reflection_archive[-50:],
            "meta_cognitive_reflections": [ref.to_dict() for ref in self.meta_cognitive_reflections[-20:]],
            "self_verification_results": [res.to_dict() for res in self.self_verification_results[-20:]],
            "evolution_goals": [goal.to_dict() for goal in self.evolution_goals],
            "curriculum_level": self.config.current_curriculum_level,
            "performance_trajectory": self.performance_trajectory,
            "strategy_adaptations": self.strategy_adaptation_count,
            "history": self.evolution_history,
            "config_used": {
                "use_intelligent_reflection": self.config.use_intelligent_reflection,
                "use_knowledge_integration": self.config.use_knowledge_integration,
                "use_candidate_merge": self.config.use_candidate_merge,
                "use_multi_objective": self.config.use_multi_objective,
                "use_system_aware_merge": self.config.use_system_aware_merge,
                "use_curriculum_learning": self.config.use_curriculum_learning,
                "use_goal_oriented_evolution": self.config.use_goal_oriented_evolution,
                "use_self_verification": self.config.use_self_verification,
                "use_meta_cognition": self.config.use_meta_cognition,
                "adaptive_mutation": self.config.adaptive_mutation,
                "frontier_size": self.config.frontier_size
            }
        }
        write_file(history_file, json.dumps(history, indent=2))
        
        summary_file = os.path.join(history_dir, 'evolution_summary.md')
        summary = f"""# Evolution Summary

## Overview
- **Initial Version**: 1
- **Final Version**: {best_candidate.version}
- **Iterations**: {self.config.max_iterations}
- **Best Fitness**: {best_candidate.overall_fitness:.2f}
- **Frontier Size**: {len(self.candidate_frontier)}
- **Lessons Learned**: {len(self.lessons_learned)}
- **Intelligent Reflection**: {'Enabled' if self.config.use_intelligent_reflection else 'Disabled'}
- **Knowledge Integration**: {'Enabled' if self.config.use_knowledge_integration else 'Disabled'}
- **System-Aware Merge**: {'Enabled' if self.config.use_system_aware_merge else 'Disabled'}
- **Curriculum Learning**: {'Enabled' if self.config.use_curriculum_learning else 'Disabled'}
- **Goal-Oriented Evolution**: {'Enabled' if self.config.use_goal_oriented_evolution else 'Disabled'}
- **Self-Verification**: {'Enabled' if self.config.use_self_verification else 'Disabled'}
- **Meta-Cognition**: {'Enabled' if self.config.use_meta_cognition else 'Disabled'}
- **Adaptive Mutation**: {'Enabled' if self.config.adaptive_mutation else 'Disabled'}
- **Final Curriculum Level**: {self.config.current_curriculum_level}
- **Strategy Adaptations**: {self.strategy_adaptation_count}

## Key Lessons
"""
        for i, lesson in enumerate(self.lessons_learned[-15:], 1):
            summary += f"{i}. {lesson}\n"
        
        if self.evolution_goals:
            summary += f"\n## Evolution Goals\n"
            achieved = sum(1 for g in self.evolution_goals if g.achieved)
            summary += f"- **Goals Achieved**: {achieved}/{len(self.evolution_goals)}\n"
            for goal in self.evolution_goals:
                status = "✓ Achieved" if goal.achieved else "○ In Progress"
                summary += f"- {status}: {goal.description}\n"
        
        if self.performance_trajectory:
            summary += f"\n## Performance Trajectory\n"
            for point in self.performance_trajectory:
                summary += f"- Iteration {point['iteration']}: Avg={point['avg_fitness']:.2f}, Best={point['best_fitness']:.2f}\n"
        
        summary += f"\n## Final Fitness Scores\n"
        for obj, score in best_candidate.fitness_scores.items():
            summary += f"- {obj.value}: {score:.2f}\n"
        
        write_file(summary_file, summary)
    
    def record_skill_usage(
        self,
        skill_content: str,
        skill_version: int,
        success: bool,
        feedback: Optional[str] = None,
        performance_metrics: Optional[Dict[str, float]] = None,
        error_messages: Optional[List[str]] = None
    ):
        """
        Record skill usage to enable continuous learning and self-evolution
        
        Args:
            skill_content: Content of the skill being used
            skill_version: Version of the skill
            success: Whether the usage was successful
            feedback: Optional user feedback
            performance_metrics: Optional performance metrics
            error_messages: Optional error messages
        """
        usage_record = {
            "timestamp": datetime.now().isoformat(),
            "skill_version": skill_version,
            "success": success,
            "feedback": feedback,
            "performance_metrics": performance_metrics or {},
            "error_messages": error_messages or [],
            "content_hash": self._compute_content_hash(skill_content)
        }
        
        self.lessons_learned.append(f"Usage v{skill_version}: {'Success' if success else 'Failed'}")
        
        if feedback:
            self.lessons_learned.append(f"Feedback: {feedback}")
        
        if error_messages:
            for error in error_messages[:3]:
                lesson = f"Address issue from v{skill_version}: {error[:100]}"
                if lesson not in self.lessons_learned:
                    self.lessons_learned.append(lesson)
        
        if len(self.lessons_learned) > 150:
            self.lessons_learned = self.lessons_learned[-150:]
        
        if self.experience_tracker:
            self._save_usage_to_experience_tracker(usage_record)
    
    def _compute_content_hash(self, content: str) -> str:
        """Compute hash of skill content for tracking"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def _save_usage_to_experience_tracker(self, usage_record: Dict[str, Any]):
        """Save usage record to experience tracker if available"""
        if not self.experience_tracker:
            return
        
        try:
            skill_id = usage_record.get('content_hash', 'unknown-skill')
            skill_version = usage_record.get('skill_version', 1)
            success = usage_record.get('success', False)
            
            outcome = InteractionOutcome.SUCCESS if success else InteractionOutcome.FAILED
            
            interaction_id = self.experience_tracker.start_interaction(
                skill_id=skill_id,
                skill_version=skill_version,
                interaction_type=InteractionType.EXECUTION
            )
            
            self.experience_tracker.complete_interaction(
                interaction_id=interaction_id,
                outcome=outcome,
                performance_metrics=usage_record.get('performance_metrics', {}),
                error_messages=usage_record.get('error_messages', []),
                user_feedback=usage_record.get('feedback')
            )
        except Exception as e:
            print(f"Failed to save to experience tracker: {e}")
    
    def evolve_from_feedback(
        self,
        skill_dir: str,
        feedback_summary: str,
        config: Optional[EvolutionConfig] = None
    ) -> str:
        """
        Evolve a skill based on accumulated usage feedback - enables self-evolution
        
        Args:
            skill_dir: Directory containing the skill
            feedback_summary: Summary of feedback to incorporate
            config: Optional evolution configuration
            
        Returns:
            Path to the evolved skill directory
        """
        if config:
            self.config = config
        
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_file):
            raise Exception(f"SKILL.md not found: {skill_file}")
        
        initial_content = read_file(skill_file)
        
        self.lessons_learned.append(f"Feedback-driven evolution: {feedback_summary}")
        
        return self.evolve_skill(skill_dir, config)
    
    def get_evolution_readiness(self) -> Dict[str, Any]:
        """
        Assess if a skill is ready for evolution based on accumulated data
        
        Returns:
            Readiness assessment with metrics and recommendations
        """
        return {
            "lessons_learned_count": len(self.lessons_learned),
            "knowledge_base_size": len(self.knowledge_base),
            "ready_for_evolution": len(self.lessons_learned) >= 3,
            "recommendations": [
                "Continue collecting usage data" if len(self.lessons_learned) < 3 
                else "Sufficient data accumulated - evolution recommended"
            ]
        }
