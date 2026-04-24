"""
Octopai - Explore, Extend, Evolve AI Agent Cognition

Comprehensive AI Agent platform with modular architecture:
- agents: Self-evolving AI agent system
- skills: Skill creation, management, and marketplace
  - creator: Multi-format skill generation (text/code/media/PPT)
  - hub: GitHub-like repository system (public/private)
- tools: Execution and orchestration
- data: Data acquisition and processing
- memory: Experience and memory management
- evolution: Advanced self-evolution engines
  - evolution_engine: Core evolution loop with frontier management
  - mutator: Skill mutation and variation generation
  - evaluator: Performance evaluation and scoring
  - feedback: Feedback history tracking
  - version_control: Checkpointing and rollback support
- tracing: Visual tracing and monitoring (OctoTrace)
  - tracer: OpenTelemetry-compatible tracing interface
  - storage: Multiple backends (in-memory, file, database)
  - visualizer: Tree/timeline visualization data
  - analytics: Performance and cost analysis
- research: Autonomous research system
  - manager: Research project and experiment management
  - models: Research data structures
"""

# Core Agents Module
from octopai.agents import (
    AgentInstance, AgentConfig, EvolvableSkill, EvolutionRun,
    TaskExecution, AgentStatus, EvolutionPhase, SkillType,
    EvolutionStrategy, FeedbackType, FeedbackSignal,
    SkillTemplate, EvolutionConfig,
    EvolutionEngineManager
)

# Skills Module
from octopai.skills import (
    SkillRegistry, RegistrySkillMetadata, SkillRegistryStatus,
    SkillFactory, SkillDefinition, SkillMetadata, SkillVersion,
    SkillHub, Skill,
    SkillBank, BankedSkill, SkillPrinciple, CommonMistake, BankSkillType,
    SkillPackager, PackageConfig,
    SkillSpec,
    SkillTemplate, TemplateLibrary
)

# Tools Module
from octopai.tools import (
    SandboxExecutor, SandboxSession, SandboxConfig, ExecutionResult, SandboxMode, ExecutionStatus,
    WorkflowEngine, WorkflowDefinition, WorkflowStep, WorkflowStepStatus,
    SubtaskOrchestrator, Subtask, SubtaskGroup, SubtaskStatus,
    OctopaiPipeline
)

# Data Module
from octopai.data import (
    WebCrawler,
    ResourceParser, ParsedResource, ResourceType, parse_resource, parse_to_skill_resource,
    URLConverter
)

# Memory Module
from octopai.memory import (
    ExperienceTracker, InteractionRecord, SkillExperience,
    ExperienceDistiller, Trajectory, TrajectoryStep, TrajectoryType, ExtractedPattern, FailureLesson,
    PersistentMemory, UserProfile, MemoryFact, UserPreference, ConversationSummary
)

# Evolution Module (Enhanced with Feedback Descent)
from octopai.evolution import (
    SkillEvolutionEngine, EvolutionConfig as SelfEvolutionConfig,
    EvolutionMode, SelectionStrategy, LoopResult,
    FrontierManager, SkillEvaluator, EvalResult,
    SkillMutator, MutationProposal, FeedbackHistory, FeedbackEntry,
    VersionManager,
    FeedbackDescentOptimizer, ComparisonResult, FDFeedbackRecord,
    Proposal, OptimizationState, create_default_proposer,
)

# Skills Creator Module
from octopai.skills.creator import (
    SkillCreator, TextParser, CodeParser, DocumentParser,
    MediaParser, PresentationParser, TemplateParser,
    SkillGenerator, SkillValidator,
    SkillCreationRequest, SkillSource, SourceType,
    GeneratedSkill, CreationResult,
    IntelligentAnalyzer, ContentAnalysis, ContentType,
)

# Skills Hub Module (Repository System - v4.0)
from octopai.skills.hub_pkg import (
    SkillRepository, RepositoryVisibility, RepositoryStatus,
    HubManager, PublishRequest, SearchResult, HubStatistics,
    PermissionManager, Role, Permission,
    MarketplaceManager, Rating, Review,
    CollaborationManager, PullRequest, Issue, Comment,
    ActivityItem, ReviewRequest, PRStatus, IssueType, IssueStatus,
)

# Program Registry Module (Skill Program Management)
from octopai.skills.program_registry import (
    ProgramRegistry,
    ProgramStatus, ProgramEntry, ProgramConfig,
    Skill, SkillMetadata, SkillType,
    Experiment
)

# Tracing Module (OctoTrace with Cost Tracking)
from octopai.tracing import (
    OctoTracer, TracerConfig, SpanKind, SpanStatus,
    Trace, Span, Session, TraceEvent,
    TraceListResult, TraceDetailResult,
    TraceStorage, InMemoryStorage, FileStorage,
    OtelTransformer, TraceVisualizer, VisualizationConfig,
    TraceAnalytics, AnalyticsReport,
    CostTracker, ModelPricing, TokenUsage,
    CostRecord, BudgetConfig,
)

# Research Module (AutoResearch - v4.0)
from octopai.research import (
    AutoResearchManager,
    ResearchProject, ResearchIdea, Experiment, Paper,
    LiteratureSearch, ResearchStatus, ExperimentStatus, Visibility,
)

__version__ = "4.0.0"

__all__ = [
    # Agents
    'AgentInstance', 'AgentConfig', 'EvolvableSkill', 'EvolutionRun',
    'TaskExecution', 'AgentStatus', 'EvolutionPhase', 'SkillType',
    'EvolutionStrategy', 'FeedbackType', 'FeedbackSignal',
    'SkillTemplate', 'EvolutionConfig',
    'EvolutionEngineManager',

    # Skills (Original)
    'SkillRegistry', 'RegistrySkillMetadata', 'SkillRegistryStatus',
    'SkillFactory', 'SkillDefinition', 'SkillMetadata', 'SkillVersion',
    'SkillHub', 'Skill',
    'SkillBank', 'BankedSkill', 'SkillPrinciple', 'CommonMistake', 'BankSkillType',
    'SkillPackager', 'PackageConfig',
    'SkillSpec',
    'SkillTemplate', 'TemplateLibrary',

    # Skills Creator (NEW)
    'SkillCreator', 'TextParser', 'CodeParser', 'DocumentParser',
    'MediaParser', 'PresentationParser', 'TemplateParser',
    'SkillGenerator', 'SkillValidator',
    'SkillCreationRequest', 'SkillSource', 'SourceType',
    'GeneratedSkill', 'CreationResult',
    'IntelligentAnalyzer', 'ContentAnalysis', 'ContentType',

    # Skills Hub (NEW - with Collaboration)
    'SkillRepository', 'RepositoryVisibility', 'RepositoryStatus',
    'HubManager', 'PublishRequest', 'SearchResult', 'HubStatistics',
    'PermissionManager', 'Role', 'Permission',
    'MarketplaceManager', 'Rating', 'Review',
    'CollaborationManager', 'PullRequest', 'Issue', 'Comment',
    'ActivityItem', 'ReviewRequest', 'PRStatus', 'IssueType', 'IssueStatus',
    
    # Program Registry (Skill Program Management)
    'ProgramRegistry',
    'ProgramStatus', 'ProgramEntry', 'ProgramConfig',
    'Skill', 'SkillMetadata', 'SkillType',
    'Experiment',

    # Tools
    'SandboxExecutor', 'SandboxSession', 'SandboxConfig', 'ExecutionResult', 'SandboxMode', 'ExecutionStatus',
    'WorkflowEngine', 'WorkflowDefinition', 'WorkflowStep', 'WorkflowStepStatus',
    'SubtaskOrchestrator', 'Subtask', 'SubtaskGroup', 'SubtaskStatus',
    'OctopaiPipeline',

    # Data
    'WebCrawler',
    'ResourceParser', 'ParsedResource', 'ResourceType', 'parse_resource', 'parse_to_skill_resource',
    'URLConverter',

    # Memory
    'ExperienceTracker', 'InteractionRecord', 'SkillExperience',
    'ExperienceDistiller', 'Trajectory', 'TrajectoryStep', 'TrajectoryType', 'ExtractedPattern', 'FailureLesson',
    'PersistentMemory', 'UserProfile', 'MemoryFact', 'UserPreference', 'ConversationSummary',

    # Evolution (Enhanced - with Feedback Descent)
    'SkillEvolutionEngine', 'SelfEvolutionConfig',
    'EvolutionMode', 'SelectionStrategy', 'LoopResult',
    'FrontierManager', 'SkillEvaluator', 'EvalResult',
    'SkillMutator', 'MutationProposal', 'FeedbackHistory', 'FeedbackEntry',
    'VersionManager',
    'FeedbackDescentOptimizer', 'ComparisonResult', 'FDFeedbackRecord',
    'Proposal', 'OptimizationState', 'create_default_proposer',

    # Tracing (OctoTrace with Cost Tracking)
    'OctoTracer', 'TracerConfig', 'SpanKind', 'SpanStatus',
    'Trace', 'Span', 'Session', 'TraceEvent',
    'TraceListResult', 'TraceDetailResult',
    'TraceStorage', 'InMemoryStorage', 'FileStorage',
    'OtelTransformer', 'TraceVisualizer', 'VisualizationConfig',
    'TraceAnalytics', 'AnalyticsReport',
    'CostTracker', 'ModelPricing', 'TokenUsage',
    'CostRecord', 'BudgetConfig',

    # Research (AutoResearch - v4.0)
    'AutoResearchManager',
    'ResearchProject', 'ResearchIdea', 'Experiment', 'Paper',
    'LiteratureSearch', 'ResearchStatus', 'ExperimentStatus', 'Visibility',
]
