"""
AI Agents Evolution Engine - Advanced Data Models
Core data structures with feedback descent and skill template support
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Callable
from enum import Enum


class AgentStatus(str, Enum):
    """Status of an agent instance"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    EVOLVING = "evolving"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"


class EvolutionPhase(str, Enum):
    """Phases in the evolution cycle"""
    ASSESSMENT = "assessment"
    IDEATION = "ideation"
    GENERATION = "generation"
    EVALUATION = "evaluation"
    INTEGRATION = "integration"
    VALIDATION = "validation"


class SkillType(str, Enum):
    """Types of evolvable skills"""
    TASK_EXECUTION = "task_execution"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    RESEARCH = "research"
    COMMUNICATION = "communication"
    TOOL_USE = "tool_use"
    CUSTOM = "custom"


class EvolutionStrategy(str, Enum):
    """Evolution strategies for different optimization approaches"""
    FEEDBACK_DESCENT = "feedback_descent"
    GRADIENT_ASCENT = "gradient_ascent"
    GENETIC_CROSSOVER = "genetic_crossover"
    MUTATION_BASED = "mutation_based"
    ENSEMBLE_EVOLUTION = "ensemble_evolution"


class FeedbackType(str, Enum):
    """Types of feedback signals in the evolution loop"""
    POSITIVE_REINFORCEMENT = "positive_reinforcement"
    NEGATIVE_CORRECTION = "negative_correction"
    NEUTRAL_OBSERVATION = "neutral_observation"
    EXPLORATORY_PROBE = "exploratory_probe"


@dataclass
class EvolutionConfig:
    """Configuration for an evolution run with advanced parameters"""
    strategy: EvolutionStrategy = EvolutionStrategy.FEEDBACK_DESCENT
    
    # Learning parameters
    learning_rate: float = 0.1
    momentum: float = 0.9
    decay_factor: float = 0.95
    
    # Exploration vs exploitation
    exploration_rate: float = 0.3
    exploitation_bias: float = 0.7
    
    # Convergence settings
    max_iterations: int = 50
    convergence_threshold: float = 0.01
    patience: int = 5
    
    # Skill generation
    max_new_skills_per_iteration: int = 3
    skill_diversity_weight: float = 0.4
    
    # Evaluation weights
    quality_weight: float = 0.35
    performance_weight: float = 0.30
    reliability_weight: float = 0.25
    novelty_weight: float = 0.10
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy.value,
            "learning_rate": self.learning_rate,
            "momentum": self.momentum,
            "decay_factor": self.decay_factor,
            "exploration_rate": self.exploration_rate,
            "exploitation_bias": self.exploitation_bias,
            "max_iterations": self.max_iterations,
            "convergence_threshold": self.convergence_threshold,
            "patience": self.patience,
            "max_new_skills_per_iteration": self.max_new_skills_per_iteration,
            "skill_diversity_weight": self.skill_diversity_weight,
            "quality_weight": self.quality_weight,
            "performance_weight": self.performance_weight,
            "reliability_weight": self.reliability_weight,
            "novelty_weight": self.novelty_weight
        }


@dataclass
class FeedbackSignal:
    """A feedback signal from task execution or evaluation"""
    signal_id: str
    source: str  # task_execution, evaluation, human_feedback, automated_test
    feedback_type: FeedbackType
    
    # Signal content
    metric_name: str
    value: float
    expected_range: tuple = (0.0, 10.0)
    
    # Context
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Processing state
    processed: bool = False
    impact_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "source": self.source,
            "feedback_type": self.feedback_type.value,
            "metric_name": self.metric_name,
            "value": round(self.value, 4),
            "expected_range": list(self.expected_range),
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "processed": self.processed,
            "impact_score": round(self.impact_score, 4)
        }


@dataclass
class SkillTemplate:
    """A reusable template for generating evolved skills"""
    template_id: str
    name: str
    category: SkillType
    
    # Template structure
    base_prompt: str
    variables: List[str] = field(default_factory=list)
    output_format: Optional[str] = None
    
    # Quality constraints
    min_quality_threshold: float = 6.0
    success_criteria: List[str] = field(default_factory=list)
    
    # Evolution metadata
    usage_count: int = 0
    success_rate: float = 0.0
    avg_quality_generated: float = 0.0
    
    # Versioning
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "category": self.category.value,
            "base_prompt": self.base_prompt,
            "variables": self.variables,
            "output_format": self.output_format,
            "min_quality_threshold": self.min_quality_threshold,
            "success_criteria": self.success_criteria,
            "usage_count": self.usage_count,
            "success_rate": round(self.success_rate, 3),
            "avg_quality_generated": round(self.avg_quality_generated, 2),
            "version": self.version,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class AgentConfig:
    """Configuration for an agent instance"""
    config_id: str
    name: str
    agent_type: str = "general"
    
    # Core parameters
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # Evolution settings
    evolution_enabled: bool = True
    auto_evolve: bool = False
    evolution_interval: int = 10
    max_iterations: int = 50
    
    # Capability bounds
    allowed_skill_types: List[str] = field(default_factory=lambda: [st.value for st in SkillType])
    safety_constraints: List[str] = field(default_factory=list)
    
    # Advanced evolution config
    evolution_config: Optional[EvolutionConfig] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "config_id": self.config_id,
            "name": self.name,
            "agent_type": self.agent_type,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "evolution_enabled": self.evolution_enabled,
            "auto_evolve": self.auto_evolve,
            "evolution_interval": self.evolution_interval,
            "max_iterations": self.max_iterations,
            "allowed_skill_types": self.allowed_skill_types,
            "safety_constraints": self.safety_constraints,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        
        if self.evolution_config:
            result["evolution_config"] = self.evolution_config.to_dict()
        
        return result


@dataclass
class EvolvableSkill:
    """A skill that can be evolved and improved"""
    skill_id: str
    name: str
    skill_type: SkillType
    description: str
    
    # Current version info
    version: str = "1.0.0"
    prompt_template: Optional[str] = None
    code_template: Optional[str] = None
    
    # Performance metrics
    success_rate: float = 0.0
    avg_execution_time: float = 0.0
    quality_score: float = 0.0
    
    # Evolution history
    evolution_count: int = 0
    last_evolved_at: Optional[datetime] = None
    
    # Status
    is_active: bool = True
    tags: List[str] = field(default_factory=list)
    
    # Advanced metrics
    adaptation_score: float = 0.0
    generalization_score: float = 0.0
    feedback_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Origin tracking
    source_template_id: Optional[str] = None
    parent_skill_id: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "skill_type": self.skill_type.value,
            "description": self.description,
            "version": self.version,
            "prompt_template": self.prompt_template,
            "code_template": self.code_template,
            "success_rate": round(self.success_rate, 3),
            "avg_execution_time": round(self.avg_execution_time, 2),
            "quality_score": round(self.quality_score, 2),
            "evolution_count": self.evolution_count,
            "last_evolved_at": self.last_evolved_at.isoformat() if self.last_evolved_at else None,
            "is_active": self.is_active,
            "tags": self.tags,
            "adaptation_score": round(self.adaptation_score, 3),
            "generalization_score": round(self.generalization_score, 3),
            "feedback_history": self.feedback_history[-10:] if self.feedback_history else [],
            "source_template_id": self.source_template_id,
            "parent_skill_id": self.parent_skill_id,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class EvolutionRun:
    """A single evolution run/cycle with full timeline"""
    run_id: str
    agent_id: str
    
    # Run metadata
    status: AgentStatus = AgentStatus.INITIALIZING
    current_phase: EvolutionPhase = EvolutionPhase.ASSESSMENT
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    evolution_config: Optional[EvolutionConfig] = None
    
    # Phases results (enhanced)
    assessment_results: Dict[str, Any] = field(default_factory=dict)
    generated_ideas: List[Dict[str, Any]] = field(default_factory=list)
    generated_skills: List[Dict[str, Any]] = field(default_factory=list)
    evaluation_results: Dict[str, Any] = field(default_factory=dict)
    integration_log: List[Dict[str, Any]] = field(default_factory=list)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    
    # Feedback signals collected during this run
    feedback_signals: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metrics
    iterations_completed: int = 0
    skills_improved: int = 0
    skills_created: int = 0
    overall_improvement: float = 0.0
    
    # Convergence tracking
    convergence_history: List[float] = field(default_factory=list)
    best_score: float = 0.0
    plateau_count: int = 0
    
    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: int = 0
    
    # Phase timing details
    phase_timings: Dict[str, int] = field(default_factory=dict)
    
    # Error handling
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "current_phase": self.current_phase.value,
            "config": self.config,
            "evolution_config": self.evolution_config.to_dict() if self.evolution_config else None,
            "assessment_results": self.assessment_results,
            "generated_ideas": self.generated_ideas,
            "generated_skills": self.generated_skills,
            "evaluation_results": self.evaluation_results,
            "integration_log": self.integration_log,
            "validation_results": self.validation_results,
            "feedback_signals": self.feedback_signals[-20:] if self.feedback_signals else [],
            "iterations_completed": self.iterations_completed,
            "skills_improved": self.skills_improved,
            "skills_created": self.skills_created,
            "overall_improvement": round(self.overall_improvement, 2),
            "convergence_history": self.convergence_history[-10:] if self.convergence_history else [],
            "best_score": round(self.best_score, 3),
            "plateau_count": self.plateau_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "phase_timings": self.phase_timings,
            "error_message": self.error_message,
            "warnings": self.warnings,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class TaskExecution:
    """Record of a task executed by an agent with enhanced tracking"""
    execution_id: str
    agent_id: str
    task_description: str
    task_type: str
    
    # Execution details
    status: str = "pending"
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    
    # Skills used
    skills_invoked: List[str] = field(default_factory=list)
    skills_generated: List[str] = field(default_factory=list)
    
    # Performance
    duration_ms: int = 0
    tokens_used: int = 0
    
    # Quality metrics
    success: bool = False
    quality_score: float = 0.0
    feedback: Optional[str] = None
    
    # Evolution trigger
    triggered_evolution: bool = False
    
    # Enhanced metrics
    complexity_score: float = 0.0
    novelty_score: float = 0.0
    efficiency_ratio: float = 0.0
    
    # Step-by-step execution log
    execution_steps: List[Dict[str, Any]] = field(default_factory=list)
    
    executed_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "agent_id": self.agent_id,
            "task_description": self.task_description,
            "task_type": self.task_type,
            "status": self.status,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "skills_invoked": self.skills_invoked,
            "skills_generated": self.skills_generated,
            "duration_ms": self.duration_ms,
            "tokens_used": self.tokens_used,
            "success": self.success,
            "quality_score": round(self.quality_score, 2),
            "feedback": self.feedback,
            "triggered_evolution": self.triggered_evolution,
            "complexity_score": round(self.complexity_score, 2),
            "novelty_score": round(self.novelty_score, 2),
            "efficiency_ratio": round(self.efficiency_ratio, 3),
            "execution_steps": self.execution_steps[-10:] if self.execution_steps else [],
            "executed_at": self.executed_at.isoformat()
        }


@dataclass
class AgentInstance:
    """Main agent instance with full evolution capabilities"""
    agent_id: str
    name: str
    config: AgentConfig
    
    # State
    status: AgentStatus = AgentStatus.IDLE
    
    # Capabilities
    skills: List[EvolvableSkill] = field(default_factory=list)
    total_skills: int = 0
    
    # History
    evolution_runs: List[EvolutionRun] = field(default_factory=list)
    task_executions: List[TaskExecution] = field(default_factory=list)
    
    # Statistics
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_quality: float = 0.0
    total_evolutions: int = 0
    total_skills_created: int = 0
    
    # Progress tracking
    current_generation: int = 1
    experience_points: float = 0.0
    
    # Enhanced analytics
    performance_trend: List[Dict[str, Any]] = field(default_factory=list)
    skill_evolution_tree: List[Dict[str, Any]] = field(default_factory=list)
    feedback_buffer: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    visibility: str = "private"
    owner_id: str = ""
    star_count: int = 0
    fork_count: int = 0
    
    created_by: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "config": self.config.to_dict(),
            "status": self.status.value,
            "skills": [skill.to_dict() for skill in self.skills],
            "total_skills": self.total_skills,
            "evolution_runs": [run.to_dict() for run in self.evolution_runs[-5:]],
            "task_executions": [exec.to_dict() for exec in self.task_executions[-10:]],
            "total_tasks_completed": self.total_tasks_completed,
            "total_tasks_failed": self.total_tasks_failed,
            "average_quality": round(self.average_quality, 3),
            "total_evolutions": self.total_evolutions,
            "total_skills_created": self.total_skills_created,
            "current_generation": self.current_generation,
            "experience_points": round(self.experience_points, 2),
            "performance_trend": self.performance_trend[-20:] if self.performance_trend else [],
            "skill_evolution_tree": self.skill_evolution_tree,
            "feedback_buffer": self.feedback_buffer[-15:] if self.feedback_buffer else [],
            "visibility": self.visibility,
            "owner_id": self.owner_id,
            "star_count": self.star_count,
            "fork_count": self.fork_count,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
